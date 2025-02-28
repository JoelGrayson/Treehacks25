const huffmanTree={
    "codes": {
      " ": "011",
      ">": "000100",
      "a": "1100",
      "b": "000101",
      "c": "10000",
      "d": "10001",
      "e": "001",
      "f": "111101",
      "g": "110100",
      "h": "11111",
      "i": "1011",
      "j": "1111001110",
      "k": "11110010",
      "l": "11011",
      "m": "00000",
      "n": "1001",
      "o": "1010",
      "p": "110101",
      "q": "11110011111",
      "r": "0100",
      "s": "0101",
      "t": "1110",
      "u": "00001",
      "v": "1111000",
      "w": "000111",
      "x": "111100110",
      "y": "000110",
      "z": "11110011110"
    },
    "tree": {
      "code": "",
      "left": {
        "code": "0",
        "left": {
          "code": "00",
          "left": {
            "code": "000",
            "left": {
              "code": "0000",
              "left": {
                "char": "m",
                "freq": 2.38,
                "code": "00000"
              },
              "right": {
                "char": "u",
                "freq": 2.55,
                "code": "00001"
              }
            },
            "right": {
              "code": "0001",
              "left": {
                "code": "00010",
                "left": {
                  "char": ">",
                  "freq": 1.151,
                  "code": "000100"
                },
                "right": {
                  "char": "b",
                  "freq": 1.4,
                  "code": "000101"
                }
              },
              "right": {
                "code": "00011",
                "left": {
                  "char": "y",
                  "freq": 1.55,
                  "code": "000110"
                },
                "right": {
                  "char": "w",
                  "freq": 1.55,
                  "code": "000111"
                }
              }
            }
          },
          "right": {
            "char": "e",
            "freq": 11.58,
            "code": "001"
          }
        },
        "right": {
          "code": "01",
          "left": {
            "code": "010",
            "left": {
              "char": "r",
              "freq": 5.86,
              "code": "0100"
            },
            "right": {
              "char": "s",
              "freq": 6.15,
              "code": "0101"
            }
          },
          "right": {
            "char": " ",
            "freq": 12.58,
            "code": "011"
          }
        }
      },
      "right": {
        "code": "1",
        "left": {
          "code": "10",
          "left": {
            "code": "100",
            "left": {
              "code": "1000",
              "left": {
                "char": "c",
                "freq": 3.13,
                "code": "10000"
              },
              "right": {
                "char": "d",
                "freq": 3.55,
                "code": "10001"
              }
            },
            "right": {
              "char": "n",
              "freq": 6.74,
              "code": "1001"
            }
          },
          "right": {
            "code": "101",
            "left": {
              "char": "o",
              "freq": 7.07,
              "code": "1010"
            },
            "right": {
              "char": "i",
              "freq": 7.08,
              "code": "1011"
            }
          }
        },
        "right": {
          "code": "11",
          "left": {
            "code": "110",
            "left": {
              "char": "a",
              "freq": 7.52,
              "code": "1100"
            },
            "right": {
              "code": "1101",
              "left": {
                "code": "11010",
                "left": {
                  "char": "g",
                  "freq": 1.75,
                  "code": "110100"
                },
                "right": {
                  "char": "p",
                  "freq": 2.0,
                  "code": "110101"
                }
              },
              "right": {
                "char": "l",
                "freq": 3.82,
                "code": "11011"
              }
            }
          },
          "right": {
            "code": "111",
            "left": {
              "char": "t",
              "freq": 8.57,
              "code": "1110"
            },
            "right": {
              "code": "1111",
              "left": {
                "code": "11110",
                "left": {
                  "code": "111100",
                  "left": {
                    "char": "v",
                    "freq": 0.99,
                    "code": "1111000"
                  },
                  "right": {
                    "code": "1111001",
                    "left": {
                      "char": "k",
                      "freq": 0.52,
                      "code": "11110010"
                    },
                    "right": {
                      "code": "11110011",
                      "left": {
                        "char": "x",
                        "freq": 0.22,
                        "code": "111100110"
                      },
                      "right": {
                        "code": "111100111",
                        "left": {
                          "char": "j",
                          "freq": 0.16,
                          "code": "1111001110"
                        },
                        "right": {
                          "code": "1111001111",
                          "left": {
                            "char": "z",
                            "freq": 0.09,
                            "code": "11110011110"
                          },
                          "right": {
                            "char": "q",
                            "freq": 0.11,
                            "code": "11110011111"
                          }
                        }
                      }
                    }
                  }
                },
                "right": {
                  "char": "f",
                  "freq": 2.23,
                  "code": "111101"
                }
              },
              "right": {
                "char": "h",
                "freq": 4.71,
                "code": "11111"
              }
            }
          }
        }
      }
    }
  };