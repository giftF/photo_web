var SwfView = {
	// ��Ҫ���ֵ�SWF�б�
	swfList: new Array(),
	// ��ӷ���
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
	// ��ʼ������
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