# last value is the nonreported value

all: values.json columns.json

values.json:
	jq '.vqlCmdResponse.layoutStatus.applicationPresModel.dataDictionary.dataSegments["1"].dataColumns[0].dataValues[9:16]' dashboard.json > $@

columns.json:
	jq '.vqlCmdResponse.layoutStatus.applicationPresModel.dataDictionary.dataSegments["1"].dataColumns[2].dataValues[29:35]' dashboard.json > $@
