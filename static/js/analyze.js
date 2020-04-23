$(function(){
	// var internel;
	// var ldumpFixItem = {"File Size": 		   "文件大小(File Size)",
	// 					"File Type":           "文件类型(File Type)",
	// 					"Compile Type":        "编译选项(Compile Type)",
	// 					"Pack Type":           "加壳种类(Pack Type)",
	// 					"Time stamp":          "创建时间(Time stamp)",
	// 					"Entry RVA":           "入口地址(Entry RVA)",
	// 					"Image base":          "基地址(Image base)",
	// 					"Object table":        "节表(Object table)",
	// 					"Main Entry RVA":      "Main入口汇编代码",
	// 					"Start Entry RVA":     "Start入口汇编代码"
	// 				};

	// // 刷新页面后，打开分析锁
	// // 无刷新上传文件，在上传文件时开锁
	// localStorage.setItem("anay", "none");

	///////////////
	// 分析文件  //
	///////////////
	$(".getinfo").click(function(){
		var anay = localStorage.getItem("anay");
		if (anay == "done")
		{
			// showDetail();
		}
		else{
			// 扫描前清除原来的DOM元素
			$(".analyze").remove();
			localStorage.setItem("anay", "done");
			var filename = localStorage.getItem("filename");
			analyzeDetail(filename);
		}
		
	});

	function analyzeDetail(filename){
		// 扫描模式
		// 设置扫描gif
		$(".gif > img").attr("src","img/scan.gif");
		// 换上绿框
		$(".analyzeShow").css("display","block");
		
		$.ajax({
			type: "POST",
			url: "analyze.php",
			data: {filename : filename},
			success: function (msg)
			{
				var result = eval("("+msg+")");
				
				if (result.length == 0) {
					showFilesizeBackup();
					return;
				}
				
				// 遍历结果，输出每一行
				for(var key in result){
					// 遍历最终输出数组，并替换内容
					for(var item in ldumpFixItem){
						// 在固定数组中找到所匹配键值
						// 原本只用一个添加即可
						// 但是为了完成多种效果，就添加了多个判断
						if (item == key) {
							// 开始添加每个条目
							if (key == "Object table" ) {
								// 只是修改节表的class
								showObjectItem(ldumpFixItem[item], result[key]);
							}
							else if ( key == "Main Entry RVA" || key == "Start Entry RVA")
							{
								// 标红第一行
								showSpecialItem(ldumpFixItem[item], result[key]);
							}
							else if ( key == "File Type" || key == "Entry RVA")
							{
								// 一定会加红的
								showNoteItem(ldumpFixItem[item], result[key]);
							}
							else if ( key == "Pack Type" || key == "Compile Type")
							{
								// 判断是否加红
								if( result[key] == "Unknown")
								{
									showItem(ldumpFixItem[item], result[key]);
								}
								else{
									showNoteItem(ldumpFixItem[item], result[key]);
								}

							}
							else{
								showItem(ldumpFixItem[item], result[key]);
							}
						}
					}
					
				}
				// 返回常态
				// 撤销绿框
				$(".analyzeShow").css("display","none");
				// 撤销文件大小bak
				$(".filesizeOut").css(
					"display", "none"
				);
				// 替换扫描图片
				$(".gif > img").attr("src","img/scanstatic.png");
				$(".analyze:even").css("background-color", "white");
			}
		});
	}

	// 添加普通元素
	function showItem(key, value){
		// $("<div>",{
		// 	"class":"analyze",
		// 	html:$("<span>",{
		// 		"class":"ldumpitem",
		// 		html:key
		// 	}).after($("<span>", {
		// 		"class":"ldumpvalue",
		// 		html:value
		// 	}))
		// }).appendTo("#tab2");
		var firstdiv = $("<div>",{
							"class":"analyze cDisplay",
							html: $("<span>",{
								"class":"ldumpitem",
								html:key
							})});

		$("#tab2").append(firstdiv);
		
		firstdiv.append($("<span>", {
				"class":"ldumpvalue",
				html:value
			}));
	}

	// 添加标红元素
	function showNoteItem(key, value){
		// $("<div>",{
		// 	"class":"analyze",
		// 	html:$("<span>",{
		// 		"class":"ldumpitem",
		// 		html:key
		// 	}).after($("<span>", {
		// 		"class":"ldumpvalue note",
		// 		html:value
		// 	}))
		// }).appendTo("#tab2");
		
		var firstdiv = $("<div>",{
							"class":"analyze cDisplay",
							html: $("<span>",{
								"class":"ldumpitem",
								html:key
							})});

		$("#tab2").append(firstdiv);
		
		firstdiv.append($("<span>", {
				"class":"ldumpvalue note",
				html: value
			}));
	}

	// 添加节表，并且标红第一行入口地址
	function showObjectItem(key, value){
		var last = value;

		// 先判断一下*的左右是不是[]
		// 如果不是，那就说明没有入口行
		if(value.slice(value.indexOf("*")+1, value.indexOf("*")+2) == ']' )
		{
			// 有入口行
			// 获得*之前的全部文本
			var firstPart = value.slice(0,value.indexOf("*")+2);

			// 得到前半部分的最后一个<br/>索引
			var lastRowIndex = firstPart.lastIndexOf(">")+1
			// 取得这个索引到*之间的值
			// 即得到所需要行的值
			var firstPart = firstPart.slice(0,lastRowIndex);

			// 获得需要行
			var needLine = value.slice(lastRowIndex, value.indexOf("*")+2);
			needLine = "<span class='note'>" + needLine + "</span>";

			last = value.slice(value.indexOf("*")+2);
			last = firstPart + needLine + last;
		}
		
		// $("<div>",{
		// 	"class":"analyze cDisplay",
		// 	html:$("<span>",{
		// 		"class":"ldumpitem",
		// 		html:key
		// 	}).after($("<span>", {
		// 		"class":"ldumpvalue",
		// 		html:last
		// 	}))
		// }).appendTo("#tab2");

		var firstdiv = $("<div>",{
							"class":"analyze cDisplay",
							html: $("<div>",{
								"class":"objectitem",
								html:key
							})});

		$("#tab2").append(firstdiv);
		
		firstdiv.append($("<div>", {
				"class":"objectvalue",
				html: last
			}));
	}

	// 添加入口地址元素，首行标红
	function showSpecialItem(key, value){
		var firstLine = value.slice(0,value.indexOf(":")+1);
		var specialData = value.slice(value.indexOf(":")+1, value.indexOf("<br"));
		var specialData = "<span class='note'>"+ specialData +"</span>";

		var last = value.slice(value.indexOf("<br"));
		var last = firstLine + specialData + last;

		// $("<div>",{
		// 	"class":"analyze cDisplay",
		// 	html:$("<span>",{
		// 		"class":"ldumpitem",
		// 		html:key
		// 	}).after($("<span>", {
		// 		"class":"ldumpvalue special",
		// 		html:last
		// 	}))
		// }).appendTo("#tab2");
		
		var firstdiv = $("<div>",{
							"class":"analyze cDisplay",
							html: $("<div>",{
								"class":"enteritem",
								html:key
							})});

		$("#tab2").append(firstdiv);
		
		firstdiv.append($("<div>", {
				"class":"entervalue special",
				html: last
			}));					
	}

	// 如果ldump崩溃，就显示原来的文件大小
	function showFilesizeBackup(){
		$(".filesizeOut").css(
			"display", "block"
		);
		// 返回常态
		// 撤销绿框
		$(".analyzeShow").css("display","none");
		// 替换扫描图片
		$(".gif > img").attr("src","img/scanstatic.png");
	}

})