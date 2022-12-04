// alert("hi");
const btn1 = document.querySelector(".btn1");
const btn2 = document.querySelector(".btn2");
const btn3 = document.querySelector(".btn3");
const sec1 = document.querySelector(".sec1");
const sec2 = document.querySelector(".sec2");
const sec3 = document.querySelector(".sec3");

btn1.addEventListener("click", () => {
    // alert("hi")
    // btn1.toggleAttribute("active");
    btn1.classList.add("bg-white");
    btn1.classList.remove("active");

    btn2.classList.add("active");
    btn3.classList.add("active");
    btn2.classList.remove("bg-white");
    btn3.classList.remove("bg-white");

    sec1.classList.remove("d-none");
    sec2.classList.add("d-none");
    sec3.classList.add("d-none");

})
btn2.addEventListener("click", () => {
    // alert("hi")
    // btn1.toggleAttribute("active");
    btn2.classList.add("bg-white");
    btn2.classList.remove("active");

    btn1.classList.add("active");
    btn3.classList.add("active");
    btn1.classList.remove("bg-white");
    btn3.classList.remove("bg-white");

    sec2.classList.remove("d-none");
    sec1.classList.add("d-none");
    sec3.classList.add("d-none");
})
btn3.addEventListener("click", () => {
    // alert("hi")
    // btn1.toggleAttribute("active");
    btn3.classList.add("bg-white");
    btn3.classList.remove("active");

    btn1.classList.add("active");
    btn2.classList.add("active");
    btn1.classList.remove("bg-white");
    btn2.classList.remove("bg-white");

    sec3.classList.remove("d-none");
    sec1.classList.add("d-none");
    sec2.classList.add("d-none");
})

var el = document.getElementById('graph'); // get canvas

var options = {
    percent:  el.getAttribute('data-percent') || 25,
    size: el.getAttribute('data-size') || 220,
    lineWidth: el.getAttribute('data-line') || 15,
    rotate: el.getAttribute('data-rotate') || 0
}

// match percentage bar

var canvas = document.createElement('canvas');
var span = document.createElement('span');
span.textContent = options.percent + '%';
console.log(options)
if (typeof(G_vmlCanvasManager) !== 'undefined') {
    G_vmlCanvasManager.initElement(canvas);
}

var ctx = canvas.getContext('2d');
canvas.width = canvas.height = options.size;

el.appendChild(span);
el.appendChild(canvas);

ctx.translate(options.size / 2, options.size / 2); // change center
ctx.rotate((-1 / 2 + options.rotate / 180) * Math.PI); // rotate -90 deg

//imd = ctx.getImageData(0, 0, 240, 240);
var radius = (options.size - options.lineWidth - 10) / 2;

var drawCircle = function(color, lineWidth, percent) {
		percent = Math.min(Math.max(0, percent || 1), 1);
		ctx.beginPath();
		ctx.arc(0, 0, radius, 0, Math.PI * 2 * percent, false);
		ctx.strokeStyle = color;
        ctx.lineCap = 'round'; // butt, round or square
		ctx.lineWidth = lineWidth
		ctx.stroke();
};
console.log(options.lineWidth)
drawCircle('#efefef', options.lineWidth, 100 / 100);
drawCircle('#0eec46', options.lineWidth + 7, options.percent / 100);