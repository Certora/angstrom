methods {
    function CalldataReaderLib.readBool(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, bool)
        => readBoolghostpair(self);
    function CalldataReaderLib.readU8(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint8)
        => readU8ghostpair(self);
    function CalldataReaderLib.readU16(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint16)
        => readU16ghostpair(self);
    function CalldataReaderLib.readU32(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint32)
        => readU32ghostpair(self);
    function CalldataReaderLib.readI24(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, int24) 
        => readI24ghostpair(self);
    function CalldataReaderLib.readU40(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint40)
        => readU40ghostpair(self);
    function CalldataReaderLib.readU64(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint64)
        => readU64ghostpair(self);
    function CalldataReaderLib.readU128(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint128)
        => readU128ghostpair(self);
    function CalldataReaderLib.readAddr(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, address)
        => readAddrghostpair(self);
    function CalldataReaderLib.readU160(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint160)
        => readU160ghostpair(self);
    function CalldataReaderLib.readU256(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, uint256)
        => readU256ghostpair(self);
    function CalldataReaderLib.readU24End(GrowthOutsideUpdater.CalldataReader self) internal returns (GrowthOutsideUpdater.CalldataReader, GrowthOutsideUpdater.CalldataReader)
        => readU24Endghostpair(self);
}
 
ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readBoolreaders;
ghost mapping (GrowthOutsideUpdater.CalldataReader => bool) readBoolvalues;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU8readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint8) readU8values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU16readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint16) readU16values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU32readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint32) readU32values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readI24readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => int24) readI24values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU40readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint40) readU40values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU64readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint64) readU64values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU128readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint128) readU128values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readAddrreaders;
ghost mapping (GrowthOutsideUpdater.CalldataReader => address) readAddrvalues;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU160readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint160) readU160values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU256readers;
ghost mapping (GrowthOutsideUpdater.CalldataReader => uint256) readU256values;

ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU24Endreaders;
ghost mapping (GrowthOutsideUpdater.CalldataReader => GrowthOutsideUpdater.CalldataReader) readU24Endends;


function readBoolghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, bool) {
    return (readBoolreaders[self], readBoolvalues[self]);
}
function readU8ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint8) {
    return (readU8readers[self], readU8values[self]);
}
function readU16ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint16) {
    return (readU16readers[self], readU16values[self]);
}
function readU32ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint32) {
    return (readU32readers[self], readU32values[self]);
}
function readI24ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, int24) {
    return (readI24readers[self],readI24values[self]);
}
function readU40ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint40) {
    return (readU40readers[self], readU40values[self]);
}
function readU64ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint64) {
    return (readU64readers[self], readU64values[self]);
}
function readU128ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint128) {
    return (readU128readers[self],readU128values[self]);
}
function readAddrghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, address) {
    return (readAddrreaders[self], readAddrvalues[self]);
}
function readU160ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint160) {
    return (readU160readers[self], readU160values[self]);
}
function readU256ghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, uint256) {
    return (readU256readers[self], readU256values[self]);
}
function readU24Endghostpair(GrowthOutsideUpdater.CalldataReader self) returns (GrowthOutsideUpdater.CalldataReader, GrowthOutsideUpdater.CalldataReader) {
    return (readU24Endreaders[self],readU24Endends[self]);
}
