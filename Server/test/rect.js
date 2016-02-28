function drawBubbleRect(context,x1,y1,w,h, radius, borderwidth,color) {

    //TODO: add styles (see through, etc)
    //CHCEK MASKS
    context.fillStyle="#6E6C6C"; //dark grey

    //draw border
    context.beginPath();
    context.moveTo(x1,y1+radius);
    context.lineTo(x1,y1+h-radius);
    context.arcTo(x1,y1+h,x1+radius,y1+h,radius);
    context.lineTo(x1+w-radius,y1+h);
    context.arcTo(x1+w,y1+h,x1+w,y1+h-radius,radius);
    context.lineTo(x1+w,y1+radius);
    context.arcTo(x1+w,y1,x1+w-radius,y1,radius);
    context.lineTo(x1+radius,y1);
    context.arcTo(x1,y1,x1,y1+radius,radius);
    context.fill();
    
    
    context.fillStyle=color; //BLUE
    context.beginPath();
    context.moveTo(x1+borderwidth,y1+radius+borderwidth);
    context.lineTo(x1+borderwidth,y1+h-radius-borderwidth);
    context.arcTo(x1+borderwidth,y1+h-borderwidth,x1+radius+borderwidth,y1+h-borderwidth,radius);
    context.lineTo(x1+w-radius-borderwidth,y1+h-borderwidth);
    context.arcTo(x1+w-borderwidth,y1+h-borderwidth,x1+w-borderwidth,y1+h-radius-borderwidth,radius);
    context.lineTo(x1+w-borderwidth,y1+radius+borderwidth);
    context.arcTo(x1+w-borderwidth,y1+borderwidth,x1+w-radius-borderwidth,y1+borderwidth,radius);
    context.lineTo(x1+radius+borderwidth,y1+borderwidth);
    context.arcTo(x1+borderwidth,y1+borderwidth,x1+borderwidth,y1+radius+borderwidth,radius);
    context.fill();
}
