# RingVote
An anonymous voting system utilizing ring signatures.

## Installation
RingVote can be installed via pip using the following command:
```shell
pip install git+https://github.com/MtCelesteMa/ringvote.git
```

RingVote utilizes the crypto-otrs library, which requires the OpenSSL library.
Prior to running RingVote for the first time, set the `CPATH` and `LIBRARY_PATH` flags to point to the OpenSSL `include` and `lib` directories respectively.
