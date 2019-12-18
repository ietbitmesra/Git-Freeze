///////////////////////////////////
///////////////////////////////////
///////including packages/////////////
var cheerio=require('cheerio');
var rp=require('request-promise');
var nodemailer = require('nodemailer');
var f=1;//used to check while writing data for the first time in JSON file
var data=[];//array to store all the required output data
var p1="",p2="";//used to get the names of the phones in required format
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
////////function to wait for some time before execurting next line////////////
////////////////////////////////////////////////////////////////////////
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
///////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////
////////mailing the user/////////
var transporter = nodemailer.createTransport({
  service: 'gmail',
  secure: true,
  port: 465,
  auth: {
    user: 'abc@gmail.com',//sender's email-id
    pass: 'password'////////sender's password
  }
});
function phone1mail(newp)//mail for phone1 price drop
{ 
    var mailOptions = {
        from: 'abc@gmail.com',//sender's email-id
        to: ['xyz@gmail.com',//receiver-1 email-id
        'pqr@gmail.com'],//////receiver-2 email-id
        subject: 'Price drop for '+ p1,
        text: 'Hey!! The price for '+p1+' has dropped to '+newp+' .Hurry up!!'
      };
      
      transporter.sendMail(mailOptions, function(error, info){
        if (error) {
          console.log(error);
        } else {
          console.log('Email sent: ' + info.response);
        }
      });
}
function phone2mail(newp)//mail for phone2 price drop
{ 
    var mailOptions = {
      from: 'abc@gmail.com',//sender's email-id
        to: ['pqr@gmail.com',///receiver-1 email-id
             'xyz@gmail.com'],//receiver-2 email-id
        subject: 'Price drop for '+ p2,
        text: 'Hey!! The price for '+p2+' has dropped to '+newp+' .Hurry up!!'
      };
      
      transporter.sendMail(mailOptions, function(error, info){
        if (error) {
          console.log(error);
        } else {
          console.log('Email sent: ' + info.response);
        }
      });
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
//////////function to read the previous price of phone1 from JSON file///////////
//////////////////////////////////////////////////////////////////
function phone1data()
{
      let fs=require('fs');
      let rawdata = fs.readFileSync('./compare2.json');
      const compare = JSON.parse(rawdata);
      let ip=compare[1]["Phone1"].slice(2);
      ip=ip.replace(",","");
      var pi=parseFloat(ip);
      return pi;
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
////////function to read previous price of phone2 from JSON file////////
///////////////////////////////////////////////////////////////////
function phone2data()
{
      let fs=require('fs');
      let rawdata = fs.readFileSync('./compare2.json');
      const compare = JSON.parse(rawdata);
      let ip=compare[1]["Phone2"].slice(2);
      ip=ip.replace(",","");
      var pi=parseFloat(ip);
      return pi;
}
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
///function to make the request and extracting the information and writing it to a JSON file////
//////////////////////////////////////////////////////////////
function main()
{
const options={
    uri:'https://www.gadgetsnow.com/compare-mobile-phones/'+p1+'-vs-'+p2,
    transform: function(body){
        return cheerio.load(body);
   }};
   rp(options).then(($)=>{
       $('.title').each(function(i,elm){////////selecting the .title class
           if((($(this).text().trim()).localeCompare("Price")==0 || ($(this).text().trim()).localeCompare("operating system")==0 || 
           ($(this).text().trim()).localeCompare("internal memory")==0 || ($(this).text().trim()).localeCompare("camera features")==0 || 
           ($(this).text().trim()).localeCompare("processor")==0 || ($(this).text().trim()).localeCompare("chipset")==0 || 
           ($(this).text().trim()).localeCompare("Chipset")==0 || ($(this).text().trim()).localeCompare("ram")==0 || 
           ($(this).text().trim()).localeCompare("rear camera")==0 || ($(this).text().trim()).localeCompare("front camera")==0 || 
           ($(this).text().trim()).localeCompare("wifi")==0 || ($(this).text().trim()).localeCompare("wifi features")==0 || 
           ($(this).text().trim()).localeCompare("bluetooth")==0  || ($(this).text().trim()).localeCompare("usb connectivity")==0 || 
           ($(this).text().trim()).localeCompare("network support")==0 || ($(this).text().trim()).localeCompare("graphics")==0))
           { 
           var title=($(this).text().trim());
           for(let i=0;i<data.length;i++) 
           {
            if(data[i].Feature === title)
             {
                return true;
             }
           }
           var phone1=($(this).next().text().trim());
           var phone2=($(this).next().next().text().trim());
           if(($(this).text().trim()).localeCompare("Price")==0)
           {
           data.unshift({Feature:title,//pushing the data to array
                      Phone1:phone1,
                      Phone2:phone2
        });
      }
        else{
            data.push({Feature:title,
                Phone1:phone1,
                Phone2:phone2
                      });
        }}
        if(($(this).text().trim()).localeCompare("Price")==0 && f!=1)//false for first time when f=1 because first time no data is written in JSON file
        {
            let previous=phone1data();//reading the previous price from JSON file
            var newprice=($(this).next().text().trim()).slice(2);//getting new price by scraping
           newprice=newprice.replace(/,/g,"");
           var newip=parseFloat(newprice);
        if(previous>newip)//comparing previous price with the new price
        {
        phone1mail($(this).next().text().trim());//mail for phone1 price drop
        }
        previous=phone2data();
        newprice=($(this).next().next().text().trim()).slice(2);
       newprice=newprice.replace(/,/g,"");
       newip=parseFloat(newprice);
    if(previous>newip)
    {
    phone2mail($(this).next().next().text().trim());//mail for phone2 price drop
    }
    }
       });
       sleep(10000);// calling sleep function to wait for 10 sec before executing next line
       data.unshift({Phone1: p1,
                  Phone2: p2});
       let fs=require('fs'),
       jsonData=JSON.stringify(data,undefined,4);
       fs.writeFile('./compare2.json',jsonData,function(err){//writing the data to JSON file
           if(err)
           console.log(err);
       });
       f=2;//it means program has run for first time
       data=[];//assigning null to array
   }).catch((err)=>{
       console.log(err);
   });
}
///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
///////////function to take input from user and excute further/////////////////////////
///////////////////////////////////////////////////////////////////////////////
function input()
{
const prompt = require('prompt-sync')();
console.log("For phone 1");
var p1brand = prompt('Brand : ').trim();
var p1model = prompt('Model : ').trim();
console.log("For phone 2");
var p2brand = prompt('Brand : ');
var p2model = prompt('Model : ');
var p1p=p1brand+"-"+p1model;
var p2p=p2brand+"-"+p2model;
p1 = p1p.replace(/ /g, "-");
p2 = p2p.replace(/ /g, "-");
setInterval(()=>main(),1000*30);//repeats after every 30 seconds
}
/////////////////////////////////////////////////
/////////////////////////////////////////////////
/////////////////////////////////////////////////
input();//////////////////////////////////////////calling the input function
///////////////////////////////////////
/////////////////////////////////////
//////////////////////////////////
///////////////////////////////
////////////////////////////
////////////////////////
/////////////////////
/////////////////
/////////////
/////////
////