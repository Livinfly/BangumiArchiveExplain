## 前言

**jsonlines** 中的 **key-value** 的标识。

以下内容为 2024-11，请自行检查时效性。

结构体类型来自 [bangumi/server/cmd/archive/main.go](https://github.com/bangumi/server/blob/b719b55ee31172054b2233de7d1827d211a2f7df/cmd/archive/main.go) ，个人注释、解释仅供参考。

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
type Character struct {							// 实体
	ID       model.CharacterID `json:"id"`		// https://bgm.tv/character/[id]
	Role     uint8             `json:"role"`	// 1角色，2机器/机甲，3战舰，4标志（猜测）
	Name     string            `json:"name"`	// 姓名
	Infobox  string            `json:"infobox"`	// 别名等，详细见 character_infobox.json
	Summary  string            `json:"summary"`	// 人物简介
	Comments uint32            `json:"comments"`// 评论/吐槽数（包含楼中楼）
	Collects uint32            `json:"collects"`// 收藏数
}
```

**infobox** 中的内容是不确定键值的，具体键值出现频率见 **character_infobox.json**。

有趣的事：用这个，发现 **wiki** 有些没有正确格式的 **infobox**，id 为 `13258` `13659` `23675` `78190` `165328`。（已报告）

## episode.jsonlines

```go
type Episode struct {								// 剧集/曲目
	ID          model.EpisodeID `json:"id"`			// https://bgm.tv/ep/[id]
	Name        string          `json:"name"`		// 名字
	NameCn      string          `json:"name_cn"`	// 简体中文名（显示于章节列表）
	Description string          `json:"description"`// 描述（常包含staff，summary）
	AirDate     string          `json:"airdate"`	// 首播日期
	Disc        uint8           `json:"disc"`		// 第[disc]张光盘
	Duration    string          `json:"duration"`	// 时长
	SubjectID   model.SubjectID `json:"subject_id"`	// 作品id https://bgm.tv/subject/[id]
	Sort        float32         `json:"sort"`		// 序话，第[sort]集
	Type        episode.Type    `json:"type"`		// 0正篇，1特别篇（番外/总集），2OP，3ED，4Trailer，5MAD，6O其他
}
```

## person.jsonlines



## person-characters.jsonlines



## subject.jsonlines



## subject-characters.jsonlines



## subject-persons.jsonlines



## subject-relations.jsonlines



数据来源：[bangumi/Archive: Wiki Data Public Archive](https://github.com/bangumi/Archive)