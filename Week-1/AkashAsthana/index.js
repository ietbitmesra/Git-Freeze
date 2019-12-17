const rp = require('request-promise');
const cheerio = require('cheerio');
const fs = require('fs');
const nodemailer = require('nodemailer');


const requiredSpecs = [
    "operating system",
    "processor",
    "battery",
    "network support",
    "weight",
    "front camera",
    "rear camera",
    "display",
    "screen size",
    "screen resolution",
    "internal memory",
    "ram",
    "price"
];

var specSheat = [];
const phone1 = process.argv[2];
const phone2 = process.argv[3];

//URL for sending requests for data
const URL = `https://www.gadgetsnow.com/compare-mobile-phones/${phone1}-vs-${phone2}`;


//Request options for specifications from gadgetsnow
const specOptions = {
    url: URL,
    json: true,
    transform: body => cheerio.load(body)
}


//Async function for checking prices every minute
async function mainFunc(specOptions) {

    let bool1 = await SpecFunc(specOptions);

    if (bool1) {

        setInterval(priceCheck, 120000);

    } else {

        console.log("ERROR");
    }

}



//Function for sending request for specifications of the smartphones
function SpecFunc(specOptions) {
    return rp(specOptions)
        .then(($) => {

            $('.title').each((i, element) => {

                var spec = $(element).text();

                if (requiredSpecs.includes((spec.toLowerCase()))) {

                    var specType = spec;
                    var phone1Val = $(element).next().text();
                    var phone2Val = $(element).next().next().text();

                    var newObj = {
                        Specification: specType.toUpperCase(),
                        Phone1: {
                            Smartphone: phone1,
                            value: phone1Val,
                        },
                        Phone2: {
                            Smartphone: phone2,
                            value: phone2Val,
                        },
                    }



                    specSheat.push(newObj);

                }
            })
            return true;

        })
        .catch((err) => {
            console.log(err);
            return false;
        })


}



//Function to check the price changes of the smartphones
function priceCheck() {

    //Message to be sent via email
    var message = "";
    var sendEmail = false;

    if (fileExists("specifications.json")) {

        var specFile = JSON.parse(fs.readFileSync('specifications.json'));

        //Original price
        var obj1 = specFile.find(obj => {
            return obj.Specification.toLowerCase() === "price";
        })

        //Price to be checked
        var obj2 = specSheat.find(obj => {
            return obj.Specification.toLowerCase() === "price";
        })


        if (priceComparison(obj1.Phone1.value, obj2.Phone1.value)) {

            console.log("Sending an email to the user for price drop");

            //Making changes to the specifications.json file
            fs.writeFileSync("specifications.json", JSON.stringify(specSheat));

            message += `The Price of ${phone2} has dropped. Checkout at ${URL}. \n`;
            sendEmail = true;
        }
        if (priceComparison(obj1.Phone2.value, obj2.Phone2.value)) {
            console.log("Sending an email to the user for price drop");

            //Making changes to the specifications.json file
            fs.writeFileSync("specifications.json", JSON.stringify(specSheat));

            message += `The Price of ${phone2} has dropped. Checkout at ${URL}. \n`;
            sendEmail = true;

        }


    } else {
        //If the file does not exists then simply write the 
        //data into the file without checking for price drops
        fs.writeFileSync("specifications.json", JSON.stringify(specSheat));
    }


    if (sendEmail) {
        console.log("Sending an email to the user for price drop");
        sendMail(message);
    } else {
        console.log("No Price Drops Yet");
    }

}



//Comparing old and new prices
function priceComparison(currentPrice, newPrice) {
    currentPrice = parseInt(currentPrice.slice(2, currentPrice.length).replace(',', ''), 10);
    newPrice = parseInt(newPrice.slice(2, newPrice.length).replace(',', ''), 10);

    return newPrice < currentPrice;
}

async function sendMail(message) {


    var transporter = nodemailer.createTransport({
        service: 'gmail',
        secure: true,
        port: 465,
        auth: {
            user: "SENDER'S EMAIL",         //Replace with sender's email
            pass: "SENDER'S PASSWORD"       //Replace with sender's password
        }
    });

    var mailOptions = {
        from: "SENDER'S EMAIL",             //Replace with sender's email
        to: "RECIEVER'S EMAIL",             //Replace with reciever's email
        subject: "Price drops in smartphones",
        text: message
    };

    await transporter.sendMail(mailOptions, function (error, info) {
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent: ' + info.response);
        }
    });

}



//Function for checking if the specifications.json file exists or not
function fileExists(fileName) {
    var path = fileName

    try {
        if (fs.existsSync(path)) {
            return true;
        } else {
            return false;
        }
    } catch (err) {
        console.error(err)
    }
}


//Calling the main function to start the application
mainFunc(specOptions);
