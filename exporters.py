import json
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ElementTree



class DataExporter(ABC):
    """Абстрактный класс (стратегия) для экспортёров данных."""

    @abstractmethod
    def export(self, data: list, columns: list, out_path: str) -> None:
        pass


class JsonExporter(DataExporter):
    """Экспорт результатов в формате JSON."""

    def export(self, data: list, columns: list, out_path: str) -> None:
        records = [dict(zip(columns, row)) for row in data]
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4, default=str)


class XmlExporter(DataExporter):
    """Экспорт результатов в формате XML."""

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
    """Фабрика для создания экспортера по названию формата."""

    @staticmethod
    def get_exporter(fmt: str) -> DataExporter:
        fmt = fmt.lower()
        if fmt == "json":
            return JsonExporter()
        elif fmt == "xml":
            return XmlExporter()
        else:
            raise ValueError(f"Неподдерживаемый формат выгрузки: {fmt}")