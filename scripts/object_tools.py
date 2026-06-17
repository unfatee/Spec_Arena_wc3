from pathlib import Path
import struct


ZERO_ID = "\x00\x00\x00\x00"


class ObjectFile:
    def __init__(self, path, leveled=False):
        self.path = Path(path)
        self.leveled = leveled
        self.data = self.path.read_bytes()
        self.pos = 0
        self.version = self.read_u32()
        self.tables = [self.read_table(), self.read_table()]
        if self.pos != len(self.data):
            raise RuntimeError(f"unparsed bytes in {self.path}: {len(self.data) - self.pos}")

    def read_u32(self):
        value = struct.unpack_from("<I", self.data, self.pos)[0]
        self.pos += 4
        return value

    def read_i32(self):
        value = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def read_f32(self):
        value = struct.unpack_from("<f", self.data, self.pos)[0]
        self.pos += 4
        return value

    def read_id(self):
        value = self.data[self.pos:self.pos + 4].decode("latin1")
        self.pos += 4
        return value

    def read_str(self):
        end = self.data.index(0, self.pos)
        value = self.data[self.pos:end].decode("utf-8", errors="replace")
        self.pos = end + 1
        return value

    def read_table(self):
        result = []
        count = self.read_u32()
        for _ in range(count):
            old = self.read_id()
            new = self.read_id()
            mod_count = self.read_u32()
            mods = []
            for _ in range(mod_count):
                field = self.read_id()
                typ = self.read_u32()
                if self.leveled:
                    level = self.read_u32()
                    data = self.read_u32()
                else:
                    level = 0
                    data = 0
                if typ == 0:
                    value = self.read_i32()
                elif typ in (1, 2):
                    value = self.read_f32()
                elif typ == 3:
                    value = self.read_str()
                else:
                    raise RuntimeError(f"unknown mod type {typ} at {self.pos} in {self.path}")
                end_id = self.read_id()
                mods.append({"field": field, "type": typ, "level": level, "data": data, "value": value, "end": end_id})
            result.append({"old": old, "new": new, "mods": mods})
        return result

    @staticmethod
    def code(obj):
        return obj["new"] if obj["new"] != ZERO_ID else obj["old"]

    def objects(self):
        for table in self.tables:
            yield from table

    def find(self, code):
        for obj in self.objects():
            if self.code(obj) == code:
                return obj
        raise RuntimeError(f"object {code} not found in {self.path}")

    def find_all(self, code):
        return [obj for obj in self.objects() if self.code(obj) == code]

    def mods(self, obj, field=None):
        if field is None:
            return obj["mods"]
        return [m for m in obj["mods"] if m["field"] == field]

    def get(self, obj, field, default=None, level=None, data=None):
        for mod in obj["mods"]:
            if mod["field"] != field:
                continue
            if level is not None and mod["level"] != level:
                continue
            if data is not None and mod["data"] != data:
                continue
            return mod["value"]
        return default

    def set(self, obj, field, value, typ=None, level=None, data=None):
        for mod in obj["mods"]:
            if mod["field"] != field:
                continue
            if level is not None and mod["level"] != level:
                continue
            if data is not None and mod["data"] != data:
                continue
            if typ is not None and mod["type"] != typ:
                raise RuntimeError(f"type mismatch for {self.code(obj)} {field}")
            mod["value"] = value
            return mod
        raise RuntimeError(f"mod {field} not found on {self.code(obj)}")

    def add_mod(self, obj, field, typ, value, level=0, data=0, end=ZERO_ID):
        obj["mods"].append({"field": field, "type": typ, "level": level, "data": data, "value": value, "end": end})

    def write(self, path=None):
        out = bytearray()
        out += struct.pack("<I", self.version)
        for table in self.tables:
            out += struct.pack("<I", len(table))
            for obj in table:
                out += obj["old"].encode("latin1")
                out += obj["new"].encode("latin1")
                out += struct.pack("<I", len(obj["mods"]))
                for mod in obj["mods"]:
                    out += mod["field"].encode("latin1")
                    out += struct.pack("<I", mod["type"])
                    if self.leveled:
                        out += struct.pack("<I", mod["level"])
                        out += struct.pack("<I", mod["data"])
                    if mod["type"] == 0:
                        out += struct.pack("<i", int(mod["value"]))
                    elif mod["type"] in (1, 2):
                        out += struct.pack("<f", float(mod["value"]))
                    elif mod["type"] == 3:
                        out += str(mod["value"]).encode("utf-8") + b"\x00"
                    else:
                        raise RuntimeError(f"unknown mod type {mod['type']}")
                    out += mod["end"].encode("latin1")
        (Path(path) if path else self.path).write_bytes(out)


def ability(path="work/war3map.w3a"):
    return ObjectFile(path, leveled=True)


def units(path="work/war3map.w3u"):
    return ObjectFile(path, leveled=False)


def items(path="work/war3map.w3t"):
    return ObjectFile(path, leveled=False)
