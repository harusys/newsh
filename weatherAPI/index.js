const line = require('@line/bot-sdk');

const config = {
    channelAccessToken: '01w2S6IaOFM1dUjij6IUlrjKduxcitRJ7kqABYEiol85eqWRQQzvqjLPps8nqyt8xTrUxr6djVRD36d+F199Ort9uOxMOwwFBP/LpsdZh6C/qOsKhlE8hItaCNo75MzF4RJNn/1f1qNH4D9+v9ixwQdB04t89/1O/w1cDnyilFU=',
    channelSecret:  '7762936b26e222adf866a4ee3ab8084e',
};


const client = new line.Client(config);
const axios = require('axios'); //追記

module.exports = async function (context, req) {
    context.log('Line Bot で受信しましたよo！.');

    if (req.query.message || (req.body && req.body.events)) {
        //テキスト以外の応答
          if (req.body &&　req.body.events[0].type !== 'message' || req.body &&　req.body.events[0].message.type !== 'text') {
          return client.replyMessage(req.body.events[0].replyToken, {
                    type: 'text',
                    text: 'テキストで入力して'
              });
            }
        //テキストの時の応答
        if (req.body && req.body.events[0]) {
                //「天気」と打った時のみの応答
                if (req.body && req.body.events[0].message.text === "天気を教えて"){                        
                        const CITY_ID = `140010`; //取得したい地域のIDを指定
                        const URL = `https://weather.tsukumijima.net/api/forecast?city=${CITY_ID}`;
                        const response = await axios.get(URL)   //"await"をつけないと，TypeError: Cannot read property 'description' of undefinedStack: ってエラーが出る．
                        const weatehrtext = response.data.description.bodyText;
                        context.log(weatehrtext);
                        message3 = {
                            type: "text",
                            text: weatehrtext
                        }
                        client.replyMessage(req.body.events[0].replyToken, message3);
                }
                //「天気」と打った時以外の応答
                else{
                    message = {
                    type: "text",
                    text: req.body.events[0].message.text //受信したメッセージをtextにセットしてる
                    }
                    message2 = {
                    type: "text",
                    text: "Hello"
                    }
                    console.log(message);
                    if (req.body.events[0].replyToken) {
                        client.replyMessage(req.body.events[0].replyToken, message);    //応答の関数
                        client.replyMessage(req.body.events[0].replyToken, message2);
                
                    }
                }
        }
        else {
            context.res = {
                status: 200,
                body: req.query.message
            };
        }
    }
    else {
        context.res = {
            status: 200,
            body: "Please check the query string in the request body"
        };
    };
};
