from xsdata.models.config import GeneratorConfig
from xsdata.codegen.transformer import SchemaTransformer
from pathlib import Path
import os

from generate_xsd_schema import gen_bindings

sdf_versions = ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]

# download the SDF templates (spare-checkout woop woop)
sdf_repo = "https://github.com/ignitionrobotics/sdformat.git"
sdf_location = Path("tools/ignition/sdformat")
current_path = os.getcwd()
try:
    sdf_location.mkdir(exist_ok=False, parents=True)
except FileExistsError:
    # has already been checked out ... ensure we are up to date
    os.chdir(sdf_location)
    os.system("git pull")
    os.chdir(current_path)
else:
    # fresh (sparse) checkout
    os.chdir(sdf_location)
    os.system(f"git clone {sdf_repo} --no-checkout . --depth 1")
    os.system("git sparse-checkout init --cone")
    os.system("git sparse-checkout set sdf")
    os.chdir(current_path)

# convert the SDF templates to XSD
xsd_location = Path("ropy/ignition/sdformat/schema/")
# sdf_versions = ["1.4", "1.5", "1.6", "1.7", "1.8"]
for version in sdf_versions:
    source_path = sdf_location / "sdf" / version
    out_dir = xsd_location / version
    out_dir.mkdir(exist_ok=True, parents=True)

    gen_bindings(source_path, out_dir, ns_prefix=f"sdformat/v{version}")

# build python bindings from XSD
config = GeneratorConfig.read(Path(__file__).parent / "sdf_bindings_config.xml")
for version in sdf_versions:
    config.output.package = (
        f"ropy.ignition.sdformat.bindings.v{version.replace('.', '')}"
    )
    source_path = xsd_location / version
    uris = [x.absolute().as_uri() for x in source_path.iterdir()]
    if uris:
        tf = SchemaTransformer(print=False, config=config)
        tf.process(uris)
