namespace cpp la
namespace php la
namespace py la

include "common.thrift"
cpp_include "common_types.h"

// tag id define
const i32 LA_TAG_PER = 1                // person
const i32 LA_TAG_LOC = 2                // place
const i32 LA_TAG_ORG = 3                // organization
const i32 LA_TAG_SFT = 4                // software
const i32 LA_TAG_GME = 5                // game
const i32 LA_TAG_SNG = 6                // song
const i32 LA_TAG_NVL = 7                // novel
const i32 LA_TAG_VDO = 8                // video
const i32 LA_TAG_STE = 9                // site
const i32 LA_TAG_BRD = 10               // brand
const i32 LA_TAG_CTN = 11               // cartoon
const i32 LA_TAG_MDL = 12               // product model
const i32 LA_TAG_PDT = 13               // product

// error number define
const i32 LA_ERR_ENC = 1                // encode error
const i32 LA_ERR_QTL = 2                // query too long error

struct LARequest
{
    1: string              query,              // query for process
    2: common.UserInfo     user_info,    // user info
    3: i32                 parse_time_switch = 0, // if != 0 , then parse time
}

service LAService
{
    common.LAResult process(1: LARequest req) throws (1:common.Exception ex)
    i32 healthy()
}
