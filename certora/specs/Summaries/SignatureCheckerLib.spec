methods {
    function SignatureCheckerLib.isValidSignatureNow(address signer, bytes32 hash, bytes memory signature) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidSignatureNowCalldata(address signer, bytes32 hash, bytes calldata signature) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidSignatureNow(address signer, bytes32 hash, bytes32 r, bytes32 vs) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidSignatureNow(address signer, bytes32 hash, uint8 v, bytes32 r, bytes32 s) internal returns (bool)  => NONDET;
    function SignatureCheckerLib.isValidERC1271SignatureNow(address signer, bytes32 hash, bytes memory signature) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidERC1271SignatureNowCalldata(address signer, bytes32 hash, bytes calldata signature) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidERC1271SignatureNow(address signer, bytes32 hash, bytes32 r, bytes32 vs) internal returns (bool) => NONDET;
    function SignatureCheckerLib.isValidERC1271SignatureNow(address signer, bytes32 hash, uint8 v, bytes32 r, bytes32 s) internal returns (bool) => NONDET;
}