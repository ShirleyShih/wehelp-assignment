// https://www.youtube.com/watch?v=6X8sDGFGRss&list=PL-g0fdC5RMbqW54tWQPIVbhyl_Ky6a2VI&index=27
// https://www.youtube.com/watch?v=zikLN9XHy4I
// document.createElement() and appendChild()

function getData(){
    let url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
    fetch(url)
        .then(function(response){
            return response.json();
        })
    
        .then(function(raw){
            const smallbox_frame=document.querySelector(".smallbox-frame");
            const bigbox_frame=document.querySelector(".bigbox-frame");

            for(let i=0;i<13/*raw.data.results.length*/;i++){
                let title=raw.data.results[i]["stitle"];
                let imageURL="https"+raw.data.results[i]["filelist"].split("https")[1];
                console.log(title,imageURL);

                if(i<3){
                    const newsmallbox=document.createElement('div');
                    newsmallbox.className='smallbox';
        
                    const newimg=document.createElement('img');
                    newimg.src=imageURL;
        
                    const newspan=document.createElement('span');
                    newspan.className='promotion';
                    newspan.innerText=title;

                    smallbox_frame.appendChild(newsmallbox);
                    newsmallbox.appendChild(newimg);
                    newsmallbox.appendChild(newspan);
                }else{
                    const newbigbox=document.createElement('div');
                    newbigbox.className='bigbox';
        
                    const newimg=document.createElement('img');
                    newimg.className='img-bg';
                    newimg.src=imageURL;
        
                    const newtitle=document.createElement('div');
                    newtitle.className='title';
                    newtitle.innerText=title;

                    const newimgstar=document.createElement('img');
                    newimgstar.className='img-star';
                    newimgstar.src="images/star.PNG";

                    bigbox_frame.appendChild(newbigbox);
                    newbigbox.appendChild(newimg);
                    newbigbox.appendChild(newtitle);
                    newbigbox.appendChild(newimgstar);
                }
            }
        })
}
getData();