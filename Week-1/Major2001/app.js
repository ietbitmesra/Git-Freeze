var request = require("request");
var cheerio = require("cheerio");
var nodeMailer = require("nodemailer");

const price = {
    iphone : 0,
    oneplus : 0
};
//Do enable third party access on your gmail account
setInterval(function(){
    request('https://www.amazon.in/Apple-iPhone-11-64GB-Black/dp/B07XVMDRZY/ref=sr_1_3?keywords=iphone+11&qid=1576689259&sr=8-3', function(err,res,body){
        if(!err && res.statusCode==200){
            const $ = cheerio.load(body);
            if(parseInt($('#priceblock_ourprice').text().slice(2).replace(',',"") < price.iphone) , 10){
                var transporter = nodeMailer.createTransport({
                    service: 'gmail',
                    auth: {
                    user: 'abcd@gmail.com',
                    pass: 'abcd'
                    }
                });
                
                var mailOptions = {
                    from: 'abcd@gmail.com',
                    to: 'xyz@gmail.com',
                    subject: 'Sending Email using Node.js',
                    text: $('#priceblock_ourprice').text() + 'is the new price of iphone 11 on Amazon'
                };
                
                transporter.sendMail(mailOptions, function(error, info){
                    if (error) {
                    console.log(error);
                    } else {
                    console.log('Email sent: ' + info.response);
                    }
                    });
            }else{
                console.log(err);
            }
            price.iphone = parseInt($('#priceblock_ourprice').text().slice(2).replace(',',"") , 10);
    };
    });
    request('https://www.amazon.in/Test-Exclusive-749/dp/B07DJ8K2KT/ref=sr_1_1?keywords=oneplus+7t+pro&qid=1576694621&smid=A23AODI1X2CEAE&sr=8-1', function(err,res,body){
        if(!err && res.statusCode==200){
            const $ = cheerio.load(body);
            if(parseInt($('#priceblock_dealprice').text().slice(2).replace(',',"") < price.oneplus) , 10){
                var transporter = nodeMailer.createTransport({
                    service: 'gmail',
                    auth: {
                    user: 'abcd@gmail.com',
                    pass: 'abcd'
                    }
                });
                
                var mailOptions = {
                    from: 'abcd@gmail.com',
                    to: 'xyz@gmail.com',
                    subject: 'Sending Email using Node.js',
                    text: $('#priceblock_ourprice').text() + 'is the new price of oneplus7t pro on Amazon'
                };
                
                transporter.sendMail(mailOptions, function(error, info){
                    if (error) {
                    console.log(error);
                    } else {
                    console.log('Email sent: ' + info.response);
                    }
                    });
            }else{
                console.log(err);
            }
            price.oneplus = parseInt($('#priceblock_dealprice').text().slice(2).replace(',',"") ,10);
            console.log(price);
        };
    });

},21600000);


    