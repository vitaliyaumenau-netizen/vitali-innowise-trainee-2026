import json
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ElementTree
from typing import ClassVar


class DataExporter(ABC):
    """Abstract class (strategy) for data exporters."""

    @abstractmethod
    def export(self, data: list, columns: list, out_path: str) -> None:
        pass


class JsonExporter(DataExporter):
    """Exports results in JSON format."""

    def export(self, data: list, columns: list, out_path: str) -> None:
        records = [dict(zip(columns, row)) for row in data]
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4, default=str)


class XmlExporter(DataExporter):
    """Exports results in XML format."""

    def export(self, data: list, columns: list, out_path: str) -> None:
        root = ElementTree.Element("results")
        for row in data:
            item = ElementTree.SubElement(root, "item")
            for col, val in zip(columns, row):
                child = ElementTree.SubElement(item, col)
                child.text = str(val) if val is not None else ""

        tree = ElementTree.ElementTree(root)
        tree.write(out_path, encoding="utf-8", xml_declaration=True)


class ExporterFactory:
    """Factory for creating an exporter based on the format name."""

    _exporters: ClassVar[dict[str, type[DataExporter]]] = {
        "json": JsonExporter,
        "xml": XmlExporter
    }

    @classmethod
    def get_exporter(cls, fmt: str) -> DataExporter:
        fmt = fmt.lower()
        exporter_class = cls._exporters.get(fmt)

        if not exporter_class:
            raise ValueError(f"Unsupported export format: {fmt}")

        return exporter_class()

    @classmethod
    def register_exporter(cls, fmt: str, exporter_class: type[DataExporter]):
        """Метод для динамического добавления новых форматов (расширения)."""
        cls._exporters[fmt.lower()] = exporter_class