namespace cpp common
namespace php common
namespace py common
//namespace lua common
namespace java net.imoran.sdk.service.common

// this thrift defines common structs used for internal interfaces between services

struct SceneInfo
{
    1:  string       page_id,            // page id
    2:  string       query_id,           // qurey id bind to this page
    3:  string       req_query_id,       // current request qurey id
    4:  i32          rank                // priority of this page, smaller value has high priority.
}

struct VoicePrint
{
    1: string        sex,
    2: string        age
}

struct UserInfo
{
    1:  string       user_id,            // user id
    2:  i64          app_id,             // app id
    3:  string       device_id,          // device id
    4:  string       user_ip,            // user ip
    5:  i32          city_id,            // user city code
    6:  double       latitude,           // user latitude
    7:  double       longitude,          // user longitude
    8:  string       app_ver,            // app version
    9:  string       account_id,         // key account id
    10: string       mor_account_id,     // moran account id
    11: string       mor_device_id,      // moran device id, unique across key
    12: string       push_user,          // user id for pushsvr
    13: VoicePrint   voice_print,
    14: string          mobile,             // user mobile phone number
    15: string          query_id,           // query id
    16: string          key                 // product key
}

// sa_result begin
struct SAToken
{
    1: string term,
    2: string pos, //为空代表没填
    3: string ner_tag, //为空代表每填
    4: i32    arc_head, //依存序列
    5: string arc_rel, //依存关系
}

// la_result begin
struct Token
{
    1: string       term,               // term
    2: string       pos,                // postag
    3: i32          pos_id,             // postagId
    4: double       weight              // weight of term
}
struct Tag
{
    1: i32          tag,                // tag id
    2: i32          offset,             // tag offset
    3: binary       bitmap,             // tag bitmap corresponding to the original query
    4: double       weight,             // tag confidence between 0~1
    5: string       uniform,            // uniform value
    6: i32          length              // tag length
}
struct LexTag
{   1:i32           token_off,
    2:i32           token_len,
    3:binary        bitset,
    4:string        tag,
    5:string        ori_text,
    6:string        val_text,
    7:double        weight
}

typedef list<LexTag> LexTagList

struct LAResult
{
    1: list<Token>  tokens,             // tokens
    2: list<Tag>    tags,                // tags
    3: list<LexTag> lex_tags            // lex parse tag
}
// la_result end

// tagging result begin

struct TaggingItem
{
    1: i32          offset,              // tag offset
    2: i32          length,             // tag length
	3: string		tag,				// tag name
	4: string		ori_text,			// tag's original value
    5: string       val_text,           // uniform value
    6: i32	weight,
}

struct TaggingResult
{
	1: list<TaggingItem> tags,			// tags
	2: list<string> terms,				// terms
	3: map<string, list<TaggingItem> > terms_tag,
}
// tagging result end


struct IntentInfo
{
    1: double                           intent_prob,            // probability for intent
    2: map<string, string>              tree_objects,           // tag to original str, i.e. tree_objects param in function FigEntityDict::create_tree()
    3: map<string, double>    detail_intent_prob,     // probability for sub and detail intents
}

struct IAResult
{
    //1:  map<IntentType, IntentInfo>    intent2result,   // result for each type
    1:  map<string, IntentInfo>    intent2result,   // result for each type
    2:  double chitchatProb,
}

struct IAResultTest
{
    1: map<string, IntentInfo>    intent2result_test,
}

// ia_result end
struct BaSlot
{
    1: string name,
    2: string value,
}

struct BaInfo
{
    1: string	intent,
    2: double	domain_prob,
    3: string   domain,
    4: list<BaSlot> slots,
}

struct BAResult
{
    1:  map<string, BaInfo>            ba2result, 
    2:  string resJson,
}

// common service request and response begin
struct Request
{
    1:  string       query,              // query for process
    2:  UserInfo     user_info,          // user info
    3:  bool         sys_msg,            // content in query is system message or user input
    4:  string       domain,             // domain restrict
    5:  bool         dialogue = true,    // do dialogue or not
    6:  LAResult     la_result,
    7:  bool         write_context = false,
    8:  string       key,                // vendor info
    9:  string       query_id,
    10: IAResult     ia_result,
    11: SceneInfo    scene,
    12: string       present_data,
    13: string       custom_data,
    14: string       app_type,           // application type for corresponding key, such as tv,soundbox,app,auto etc.
    15:  string      version,            // protocol version
    16: string       req_from,               // request source, reserved values: mortv
}
struct Response
{
    1: i32                  state,      // interactive state
    2: string               reply,      // either a direct answer or an ask to confirm something
    3: string               info,
    4: string               tts,
    5: string               json,
    6: double               score,        // confidence score
    7: string               service_name, // internal service where this response comes from
    8: string               global_context, // context info used to update to um
    9: string               corefer_context, // context info used to update to um
    10: bool                baike_tag = false, // se-baike set this tag
    11: map<string,i32>     latency,         // performance stats.
    12:  bool               cache_tag = false,
}
exception Exception
{
    1: i32          err_num,            // error number
    2: string       message             // error message
}
// common service request and response end
