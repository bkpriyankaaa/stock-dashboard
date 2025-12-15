
function initializeDashboard(subs){
    const socket = io();
    socket.on("price_update", data=>{
        subs.forEach(stock=>{
            const card=document.getElementById(stock);
            if(!card) return;
            const priceTag=card.querySelector(".price");
            const old=parseFloat(priceTag.innerText)||0;
            const now=data[stock];
            priceTag.innerText=now;
            if(now>old){card.classList.add("green");setTimeout(()=>card.classList.remove("green"),300);}
            else if(now<old){card.classList.add("red");setTimeout(()=>card.classList.remove("red"),300);}
        })
    });
}
