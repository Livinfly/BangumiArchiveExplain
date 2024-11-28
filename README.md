## 前言

**jsonlines** 中的 **key-value** 的标识。

以下内容为 2024-11，请自行检查时效性。

~~做到一半，自己眼瞎没看见~~ [bangumi/dev-docs: development documents / 开发文档](https://github.com/bangumi/dev-docs) 中有部分内容是有说明的，不过考虑到没有完全对应的 **Archive** 的对照，还是做完且做个链接过去好了。

导出数据来源：[bangumi/Archive: Wiki Data Public Archive](https://github.com/bangumi/Archive) 。

结构体类型来自 [bangumi/server/cmd/archive/main.go](https://github.com/bangumi/server/blob/b719b55ee31172054b2233de7d1827d211a2f7df/cmd/archive/main.go) ，个人注释、解释仅供参考，详细内容请参考源代码。

[bangumi/dev-docs](https://github.com/bangumi/dev-docs/tree/master) 中的 `.md` 文件亦有网站数据库相关的键值对含义参考。

职位、条目关系等定义见 [bangumi/server](https://github.com/bangumi/server) 中 `/pkg/vars` 下的 **platform** ，**relation** ，**staff** 等文件。

```shell
# 文件结构
bangumi-2024-11-19
        character.jsonlines
        episode.jsonlines
        person-characters.jsonlines
        person.jsonlines
        subject-characters.jsonlines
        subject-persons.jsonlines
        subject-relations.jsonlines
        subject.jsonlines
```

## character.jsonlines

```go
type Character struct {                          // 实体
    ID       model.CharacterID `json:"id"`       // 实体id https://bgm.tv/character/[id]
    Role     uint8             `json:"role"`     // 1角色，2机器/机甲，3战舰，4标志（猜测）
    Name     string            `json:"name"`     // 姓名
    Infobox  string            `json:"infobox"`  // 别名等，详细见 character_infobox.json
    Summary  string            `json:"summary"`  // 简介
    Comments uint32            `json:"comments"` // 评论/吐槽数（含楼中楼）
    Collects uint32            `json:"collects"` // 收藏数
}
```

**infobox** 中的内容是不确定键值的，具体键值出现频率见 **character_infobox.json**。

统计频率的代码见 **character_jsonlines.py** 。

有趣的事：用这个，发现 **wiki** 有些没有正确格式的 **infobox**，id 为 `13258` `13659` `23675` `78190` `165328`。（已报告）

## episode.jsonlines

```go
type Episode struct {                                // 剧集/曲目
    ID          model.EpisodeID `json:"id"`          // 剧集/曲目id https://bgm.tv/ep/[id]
    Name        string          `json:"name"`        // 名字
    NameCn      string          `json:"name_cn"`     // 简体中文名（显示于章节列表）
    Description string          `json:"description"` // 描述（常包含staff，summary）
    AirDate     string          `json:"airdate"`     // 首播日期
    Disc        uint8           `json:"disc"`        // 第[disc]张光盘
    Duration    string          `json:"duration"`    // 时长
    SubjectID   model.SubjectID `json:"subject_id"`  // 作品id https://bgm.tv/subject/[id]
    Sort        float32         `json:"sort"`        // 序话，第[sort]集
    Type        episode.Type    `json:"type"`        // 0正篇，1特别篇（番外/总集），2OP，3ED，4Trailer，5MAD，6O其他
}
```

## person-characters.jsonlines

```go
type PersonCharacter struct {                           // 人物-角色（作品）
    PersonID    model.PersonID    `json:"person_id"`    // 人物id https://bgm.tv/person/[id]
    SubjectID   model.SubjectID   `json:"subject_id"`   // 参与作品id https://bgm.tv/subject/[id]
    CharacterID model.CharacterID `json:"character_id"` // 对应作品中的角色id https://bgm.tv/character/[id]
    Summary     string            `json:"summary"`      // 概要（空）
}
```

## person.jsonlines

```go
type Person struct {                          // 人物
    ID       model.PersonID `json:"id"`       // 人物id https://bgm.tv/person/[id]
    Name     string         `json:"name"`     // 名字
    Type     uint8          `json:"type"`     // 1 2 3，不太看得出来是分类
    Career   []string       `json:"career"`   // 职业
    Infobox  string         `json:"infobox"`  // 别名等
    Summary  string         `json:"summary"`  // 简介
    Comments uint32         `json:"comments"` // 评论/吐槽数（含楼中楼）
    Collects uint32         `json:"collects"` // 收藏数
}
```

**infobox** 统计频率见 **person_infobox.json** 。

**career** 统计频率见 **person_career.json** 。

**type-career** 统计频率见 **person_type_career.json** 。

统计频率的代码见 **person_jsonlines.py** 。

## subject-characters.jsonlines

```go
type SubjectCharacter struct {                          // 作品-角色
    CharacterID model.CharacterID `json:"character_id"` // 角色id https://bgm.tv/character/[id]
    SubjectID   model.SubjectID   `json:"subject_id"`   // 作品id https://bgm.tv/subject/[id]
    Type        uint8             `json:"type"`         // 1主角，2配角，3客串
    Order       uint16            `json:"order"`        // 作品角色列表排序(type, order)，不保证order连续。
}
```

## subject-persons.jsonlines

```go
type SubjectPerson struct {                       // 作品-人物
    PersonID  model.PersonID  `json:"person_id"`  // 人物id https://bgm.tv/person/[id]
    SubjectID model.SubjectID `json:"subject_id"` // 作品id https://bgm.tv/subject/[id]
    Position  uint16          `json:"position"`   // 担任职位
}
```

[职位对应表](https://github.com/bangumi/server/blob/c72c7a4704565500af54d411550ce15af92fa2ed/pol/db/_const.py#L11)或见最新 [bangumi/server](https://github.com/bangumi/server) 的`/pkg/vars` **staff** 。

## subject-relations.jsonlines

```go
type SubjectRelation struct {                                    // 作品-作品
    SubjectID        model.SubjectID `json:"subject_id"`         // 作品id https://bgm.tv/subject/[id]
    RelationType     uint16          `json:"relation_type"`      // 关联类型
    RelatedSubjectID model.SubjectID `json:"related_subject_id"` // 关联作品id https://bgm.tv/subject/[id]
    Order            uint16          `json:"order"`              // 关联排序
}
```

## subject.jsonlines

```go
type Subject struct {                            // 作品
    ID       model.SubjectID   `json:"id"`       // 作品id https://bgm.tv/subject/[id]
    Type     model.SubjectType `json:"type"`     // 1漫画，2动画，3音乐，4游戏，6三次元
    Name     string            `json:"name"`     // 名字
    NameCN   string            `json:"name_cn"`  // 简体中文名
    Infobox  string            `json:"infobox"`  // 别名等
    Platform uint16            `json:"platform"` // 媒介（类别）见 server/pkg/vars/platform
    Summary  string            `json:"summary"`  // 简介
    Nsfw     bool              `json:"nsfw"`     // 是否 Nsfw

    Tags         []Tag    `json:"tags"`          // 公共标签
    Score        float64  `json:"score"`         // 评分
    ScoreDetails Score    `json:"score_details"` // 评分细节
    Rank         uint32   `json:"rank"`          // 类别内排名
    Date         string   `json:"date"`          // 发行日期
    Favorite     Favorite `json:"favorite"`      // 收藏状态（想看、看过、在看、搁置、抛弃）

    Series bool `json:"series"`                  // 系列（单行本？）
}
```