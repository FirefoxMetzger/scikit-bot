from xml.etree import ElementTree
from lxml import etree
from pathlib import Path
import argparse
from typing import Dict, Optional, List
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from dataclasses import dataclass, field
from copy import deepcopy

xs = "http://www.w3.org/2001/XMLSchema"

def _to_xsd_type(in_type: str) -> str:
    known_types = {
        "unsigned int": "xs:unsignedInt",
        "unsigned long": "xs:unsignedLong",
        "bool": "xs:boolean",
        "string": "xs:string",
        "double": "xs:double",
        "int": "xs:int",
        "float": "xs:float",
        "char": "xs:char",
        "vector3": "types:vector3",
        "vector2d": "types:vector2d",
        "vector2i": "types:vector2i",
        "pose": "types:pose",
        "time": "types:time",
        "color": "types:color",
        "sdf:sdf": "sdf:sdf",
        "world:world": "world:world",
        "scene:scene": "scene:scene",
        "state:state": "state:state",
        "physics:physics": "physics:physics",
        "light:light": "light:light",
        "actor:actor": "actor:actor",
        "model:model": "model:model",
        "link:link": "link:link",
        "sensor:sensor": "sensor:sensor",
        "joint:joint": "joint:joint",
        "collision:collision": "collision:collision",
        "visual:visual": "visual:visual",
        "material:material": "material:material",
        "geometry:geometry": "geometry:geometry"
    }

    try:
        return known_types[in_type]
    except KeyError:
        raise RuntimeError(f"Unknown type: {in_type}") from None


@dataclass
class SdfElement:
    required: str = field(
        metadata={
            "type":"Attribute",
            "namespace": ""
        }
    )

    minOccurs: str = field(init=False)
    maxOccurs: str = field(init=False)

    def __post_init__(self):
        required_codes = {
            "0": ("0", "1"),
            "1": ("1", "1"),
            "+": ("1", "unbounded"),
            "*": ("0", "unbounded"),
            "-1": ("0", "0"),
        }
        self.minOccurs, self.maxOccurs = required_codes[self.required]

@dataclass
class Element(SdfElement):
    class Meta:
        name = "element"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    copy_data: Optional[bool] = field(
        default=False,
        metadata={
            "type": "Attribute",
            "namespace": ""
        }
    )

    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": ""
        }
    )

    attribute: List["Attribute"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": ""
        }
    )

    include: List["Include"] = field(
        default_factory=list,
        metadata={
            "type":"Element",
            "namespace": ""
        }
    )

    element: List["Element"] = field(
        default_factory=list,
        metadata={
            "type":"Element",
            "namespace": ""
        }        
    )

    def __post_init__(self):

        return super().__post_init__()

    def to_xsd(self) -> etree.Element:
        if self.copy_data:
            # special element for plugin.sdf to
            # declare that any children are allowed
            subtree = etree.Element(f"{{{xs}}}any")
            subtree.set("processContents", "skip")
        else:
            subtree = etree.Element(f"{{{xs}}}element")
            subtree.set("name", self.name)
        subtree.set("minOccurs", self.minOccurs)
        subtree.set("maxOccurs", self.maxOccurs)

        if self.description:
            annotation = etree.SubElement(subtree, f"{{{xs}}}annotation")
            documentation = etree.SubElement(annotation, f"{{{xs}}}documentation")
            documentation.set("{http://www.w3.org/XML/1998/namespace}lang", "en")
            documentation.text = self.description.strip().replace("\r\n", " ").replace("\n", " ")

        if self.copy_data:
            pass  # skip
        elif self.ref:
            subtree.set("ref", f"{self.name}")
        elif self.type and len(self.element) > 0:
            raise NotImplementedError()
        elif self.type and len(self.attribute) > 0:
            complex_type = etree.SubElement(subtree, f"{{{xs}}}complexType")
            simple_content = etree.SubElement(complex_type, f"{{{xs}}}simpleContent")
            extension = etree.SubElement(simple_content, f"{{{xs}}}extension")
            extension.set("base", _to_xsd_type(self.type))
            for attribute in self.attribute:
                complex_type.append(attribute.to_xsd())
        elif self.type:
            subtree.set("type", _to_xsd_type(self.type))
        elif len(self.element) > 0:
            complex_type = etree.SubElement(subtree, f"{{{xs}}}complexType")
            
            if self.description:
                annotation = etree.SubElement(complex_type, f"{{{xs}}}annotation")
                documentation = etree.SubElement(annotation, f"{{{xs}}}documentation")
                documentation.set("{http://www.w3.org/XML/1998/namespace}lang", "en")
                documentation.text = self.description.strip().replace("\r\n", " ").replace("\n", " ")

            all_element = etree.SubElement(complex_type, f"{{{xs}}}all")
            for el in self.element:
                all_element.append(el.to_xsd())

            for attrib in self.attribute:
                complex_type.append(attrib.to_xsd())            
        else:
            subtree.set("type", _to_xsd_type("string"))

        return subtree

@dataclass
class Include(SdfElement):
    class Meta:
        name = "include"

    filename: str = field(
        metadata={
            "type":"Attribute",
            "namespace": "",
        }
    )

    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": ""
        }
    )


@dataclass
class Attribute:
    class Meta:
        name = "attribute"

    name: str = field(
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    type: str = field(
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    required: str = field(
        metadata={
            "type":"Attribute",
            "namespace": ""
        }
    )
    use: str = field(
        init=False
    )

    default: Optional[str] = field(
        metadata={
            "type": "Attribute",
            "namespace": "",
        },
    )

    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": ""
        }
    )

    def __post_init__(self):
        if self.required == "1":
            self.use = "required"
        else:
            self.use = "optional"


    def to_xsd(self) -> etree.Element:
        attrib = etree.Element(f"{{{xs}}}attribute")
        attrib.set("name", self.name)
        attrib.set("type", _to_xsd_type(self.type))
        attrib.set("use", self.use)

        if self.default and self.use == "optional":
            attrib.set("default", self.default)

        if self.description:
            annotation = etree.SubElement(attrib, f"{{{xs}}}annotation")
            documentation = etree.SubElement(annotation, f"{{{xs}}}documentation")
            documentation.set("{http://www.w3.org/XML/1998/namespace}lang", "en")
            documentation.text = self.description.strip().replace("\r\n", " ").replace("\n", " ")

        return attrib


def gen_bindings(source_dir: Path, out_dir: Path, ns_prefix="sdformat"):
    # copy the special type definitions, but add the namespace declarations
    ElementTree.register_namespace("xs", xs)
    types_file = source_dir / "schema" / "types.xsd"
    if not types_file.exists():
        types_file = Path(__file__).parent / "fallback_types.xsd"
    types_xsd = ElementTree.parse(types_file)
    types_xsd.getroot().attrib.update({
        "xmlns": f"{ns_prefix}/types.xsd",
        "targetNamespace": f"{ns_prefix}/types.xsd"
    })
    types_string = ElementTree.tostring(types_xsd.getroot())
    types_xsd = etree.fromstring(types_string)

    for el in types_xsd.findall(".//xs:restriction", namespaces={"xs": xs}):
        prefix, attrib_type = el.attrib["base"].split(":")
        el.attrib["base"] = "xs:"+attrib_type

    with open(out_dir / ("types.xsd"), "wb") as out_file:
        etree.ElementTree(types_xsd).write(out_file)


    # use a fixed set of namespaces that matches the menu structure of the SDF
    # spec. This leads to nicer bindings the schema location
    full_filename_map = {
        "root.sdf": "sdf.xsd",
        "world.sdf": "world.xsd",
        "scene.sdf": "scene.xsd",
        "state.sdf": "state.xsd",
        "physics.sdf": "physics.xsd",
        "light.sdf": "light.xsd",
        "actor.sdf": "actor.xsd",
        "model.sdf": "model.xsd",
        "link.sdf": "link.xsd",
        "sensor.sdf": "sensor.xsd",
        "joint.sdf": "joint.xsd",
        "collision.sdf": "collision.xsd",
        "visual.sdf": "visual.xsd",
        "material.sdf": "material.xsd",
        "geometry.sdf": "geometry.xsd",
    }
    filename_map = {key:value for key, value in full_filename_map.items() if (source_dir / key).exists()}

    namespaces = {
        "types": f"{ns_prefix}/types.xsd",
        "xs": "http://www.w3.org/2001/XMLSchema",

        "sdf": f"{ns_prefix}/sdf.xsd",
        "world": f"{ns_prefix}/world.xsd",
        "scene": f"{ns_prefix}/scene.xsd",
        "state": f"{ns_prefix}/state.xsd",
        "physics": f"{ns_prefix}/physics.xsd",
        "light": f"{ns_prefix}/light.xsd",
        "actor": f"{ns_prefix}/actor.xsd",
        "model": f"{ns_prefix}/model.xsd",
        "link": f"{ns_prefix}/link.xsd",
        "sensor": f"{ns_prefix}/sensor.xsd",
        "joint": f"{ns_prefix}/joint.xsd",
        "collision": f"{ns_prefix}/collision.xsd",
        "visual": f"{ns_prefix}/visual.xsd",
        "material": f"{ns_prefix}/material.xsd",
        "geometry": f"{ns_prefix}/geometry.xsd",
    }


    xml_ctx = XmlContext()
    sdf_parser = XmlParser(context=xml_ctx)
    def _parse_sane(in_file:Path) -> Element:
        root:etree.Element = etree.parse(str(in_file)).getroot()
        for description in root.findall(".//description"):
            if description.text is None:
                description.text = ""
            text:str = description.text 
            for child in [x for x in description]:
                text += etree.tostring(child).decode("UTF-8")
                description.remove(child)
            
            text = text.replace("<", "&lt;").replace(">", "&gt;")
            if text == "":
                description.text = None
            else:
                description.text = text
        xml_string = etree.tostring(root).decode("UTF-8")
        return sdf_parser.from_string(xml_string, Element)



    for in_file, out_file in filename_map.items():
        sdf_root:Element = _parse_sane(source_dir / in_file)

        queue = [sdf_root]

        while queue:
            el = queue.pop(0)
            for include in el.include:
                included_el = _parse_sane(source_dir / include.filename)
                
                if include.description:
                    included_el.description = include.description

                if include.filename in filename_map.keys():
                    # this element will be converted in it's own file
                    # nullify children and set appropriate namespace ref
                    included_el.required = include.required
                    included_el.type = included_el.name + ":" + included_el.name
                    included_el.element = list()
                    included_el.include = list()
                    included_el.attribute = list()
                
                el.element.append(included_el)

            queue.extend(el.element)

        local_ns = namespaces.copy()
        local_ns[None] = local_ns.pop(sdf_root.name)
        xsd_root = etree.Element(f"{{{xs}}}schema", nsmap=local_ns)
        xsd_root.set("targetNamespace", local_ns[None])
        xsd_root.set("version", "1.1")

        # convert the full element and then pop the outer layer
        # as we are only interested in the nested complex type
        xsd_element = sdf_root.to_xsd()
        xsd_type:etree.Element = xsd_element.find(f"./{{{xs}}}complexType")
        name = xsd_element.attrib["name"]
        xsd_type.set("name", name)
        xsd_root.append(xsd_type)

        # convert ref to typedef
        # potentially pulling out a type when needed
        for ref_el in xsd_type.findall(f".//*[@ref]"):
            ref_name = ref_el.attrib["ref"]

            if ref_name == name:
                ref_el.attrib.pop("ref")
                ref_el.set("type", name)
            else:
                for candidate in xsd_type.findall(f".//{{{xs}}}element[@name='{ref_name}']"):
                    all_children = candidate.findall(".//*")
                    if not ref_el in all_children:
                        continue

                    # promote nested type to schema level
                    referred_type = candidate.find(f"./{{{xs}}}complexType")
                    referred_type.set("name", ref_name)
                    xsd_root.append(referred_type)

                    candidate.set("type", ref_name)
                    ref_el.attrib.pop("ref")
                    ref_el.set("type", ref_name)

                    break
                else:
                    raise RuntimeError("Could not find referred element.")

        keep_ns = list()
        for type_el in xsd_root.findall(".//*[@type]"):
            element_type = type_el.attrib["type"]
            if ":" in element_type:
                prefix, _ = type_el.attrib["type"].split(":")
                keep_ns.append(prefix)
        for type_el in xsd_root.findall(".//*[@base]"):
            element_type = type_el.attrib["base"]
            if ":" in element_type:
                prefix, _ = type_el.attrib["base"].split(":")
                keep_ns.append(prefix)

        etree.cleanup_namespaces(xsd_root, keep_ns_prefixes=list(set(keep_ns)))
        used_ns = xsd_root.nsmap
        used_ns.pop("xs")

        for _, uri in used_ns.items():
            import_el = etree.Element(f"{{{xs}}}import")
            import_el.set("namespace", uri)
            file_name = Path(uri).stem + ".xsd"
            import_el.set("schemaLocation", f"./{file_name}")
            xsd_root.insert(0, import_el)
        
        if not out_dir.exists():
            out_dir.mkdir(exist_ok=True, parents=True)

        # write type file
        with open(out_dir / out_file, "wb") as out:
            etree.ElementTree(xsd_root).write(out, pretty_print=True)
