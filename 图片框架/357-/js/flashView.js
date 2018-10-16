function loadFlashView() {
	SwfView.Add("flash/index.swf", "fpv", "swfDIV", "660", "290", "8.0.0.0", "#000", {
	bigPhotoList: "images/b/1.jpg,images/b/2.jpg,images/b/3.jpg,images/b/4.jpg,images/b/5.jpg,images/b/6.jpg,images/b/7.jpg,images/b/8.jpg,images/b/9.jpg",
	smallPhotoList: "images/s/1.jpg,images/s/2.jpg,images/s/3.jpg,images/s/4.jpg,images/s/5.jpg,images/s/6.jpg,images/s/7.jpg,images/s/8.jpg,images/s/9.jpg",
	sourcePhotoList: "http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/,http://www.lanrentuku.com/", itemOverTime: 100, viewTime: 5000
	}, {scale: "noscale", allowScriptAccess: "always", wmode: "transparent"});
	SwfView.Init();
	}