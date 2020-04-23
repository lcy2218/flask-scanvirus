// 检测IE版本
function ieversion(){
	
}

// 如果是ie6，就对链接重定向
function jumpIE6()
{
	var iev = ieversion();
	if (iev == 6) {
		window.location.href="./indexie6.html";
	}
}

jumpIE6();