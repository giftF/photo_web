var SwfView = {
	// 需要呈现的SWF列表
	swfList: new Array(),
	// 添加方法
	// SwfView.Add("test.swf", "swfBox", "200", "100", "7", "#ffffff");
	Add: function (sURL, sID, sPID, nWidth, nHeight, nVersion, sBGColor, oVar, oParam) {
		if(sURL && sPID) {
			this.swfList[this.swfList.length] = {
				sURL: sURL,
				sID: sID,
				sPID: sPID,
				nWidth: nWidth,
				nHeight: nHeight,
				nVersion: nVersion,
				sBGColor: sBGColor,
				oVar: oVar,
				oParam: oParam
			}
		}
	},
	// 初始化方法
	Init: function () {
		var so;
		var list = this.swfList;
		for(var i = 0; i < list.length; i ++) {
			so = new SWFObject(list[i]["sURL"], list[i]["sID"], list[i]["nWidth"], list[i]["nHeight"], list[i]["nVersion"], list[i]["sBGColor"]);
			if(list[i]["oVar"]) {
				for(var key in list[i]["oVar"]) {
					so.addVariable(key, list[i]["oVar"][key]);
				}
			}
			if(list[i]["oParam"]) {
				for(var key in list[i]["oParam"]) {
					so.addParam(key, list[i]["oParam"][key]);
				}
			}
			so.write(list[i]["sPID"]);
		}
		list = new Array();
	}
};