from xsdata.models.config import GeneratorConfig
from xsdata.codegen.transformer import SchemaTransformer
from pathlib import Path

sdf_location = Path("~/workspace/build/sdformat11/sdf/").expanduser()
versions = ["1.0", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]

config = GeneratorConfig.read(Path(__file__).parent / "sdf_bindings_config.xml")

for version in versions:
    config.output.package = f"ropy.ignition.sdformat.models.v{version.replace('.', '')}"
    source_path = sdf_location / version

    uris = [x.as_uri() for x in source_path.iterdir() if x.suffix == ".xsd"]
    if uris:
        tf = SchemaTransformer(print=False, config=config)
        tf.process(uris)
