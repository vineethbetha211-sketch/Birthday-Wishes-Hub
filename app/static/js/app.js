// Simple utility: copy share URL
function copyShareUrl(){
    const el = document.getElementById("shareUrl");
    if(!el) return;
    el.select();
    el.setSelectionRange(0, 99999);
    try{
        document.execCommand("copy");
    }catch(e){}
}
window.copyShareUrl = copyShareUrl;

// Minimal confetti implementation (no external libs)
function launchConfetti(durationMs=1800){
    let canvas = document.getElementById("confettiCanvas");
    if(!canvas){
        canvas = document.createElement("canvas");
        canvas.id = "confettiCanvas";
        document.body.appendChild(canvas);
    }
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;

    function resize(){
        canvas.width = window.innerWidth * dpr;
        canvas.height = window.innerHeight * dpr;
        canvas.style.width = window.innerWidth + "px";
        canvas.style.height = window.innerHeight + "px";
        ctx.scale(dpr, dpr);
    }

    // Reset transform each time to avoid compounding scale
    ctx.setTransform(1,0,0,1,0,0);
    resize();
    window.addEventListener("resize", () => {
        ctx.setTransform(1,0,0,1,0,0);
        resize();
    });

    const pieces = [];
    const colors = ["#ffffff", "#cfd8ff", "#ffd1f1", "#d2fff6", "#fff2c7"];
    const count = 120;

    for(let i=0;i<count;i++){
        pieces.push({
            x: Math.random() * window.innerWidth,
            y: -20 - Math.random()*window.innerHeight*0.3,
            r: 4 + Math.random()*6,
            vy: 2 + Math.random()*4,
            vx: -1.5 + Math.random()*3,
            rot: Math.random()*Math.PI,
            vr: -0.1 + Math.random()*0.2,
            color: colors[Math.floor(Math.random()*colors.length)],
            alpha: 0.8 + Math.random()*0.2
        });
    }

    const start = performance.now();

    function frame(t){
        const elapsed = t - start;
        ctx.clearRect(0,0, window.innerWidth, window.innerHeight);

        pieces.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.rot += p.vr;
            p.vy += 0.02;
            p.alpha = Math.max(0, p.alpha - 0.0008);

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.r/2, -p.r/2, p.r, p.r*1.6);
            ctx.restore();
        });

        if(elapsed < durationMs){
            requestAnimationFrame(frame);
        }else{
            canvas.remove();
        }
    }
    requestAnimationFrame(frame);
}

// Reveal interaction
document.addEventListener("DOMContentLoaded", () => {
    const revealBox = document.getElementById("revealBox");
    if(revealBox){
        revealBox.addEventListener("click", () => {
            const enabled = window.BWH_REVEAL_ENABLED !== false;
            revealBox.classList.add("revealed");
            if(enabled){
                launchConfetti();
            }
        });
    }
});
