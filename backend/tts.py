from flask import send_file
import boto3
region_name = 'ap-northeast-2'
polly_client = boto3.client(
    'polly',
    aws_access_key_id = 'AKIAU6ECZPVOP6A4VROO',
    aws_secret_access_key = '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',
    region_name = region_name
)
korean = {
    "0": " ",
    "1": "하나",
    "2": "둘",
    "3": "셋",
    "4": "넷",
    "5": "다섯", 
    "6": "여섯",
    "7": "일곱",
    "8": "여덟",
    "9": "아홉",
    "10": "열"
}

class TTS:
    precount = 0
    def textToSpeech(self, count):
        if count != 0:
            num = (count-1)%10 + 1
        text = " "
        if TTS.precount != count:
            text = korean[str(num)]
            TTS.precount = count
        # text = korean[str(num)]
        print("TTS.precount: ", TTS.precount)
        print("count: ", count, "num: ", num)
        print("text: ", text)
        response = polly_client.synthesize_speech(
            Text="<speak>" + text + "</speak>",
            VoiceId='Seoyeon',
            OutputFormat='mp3',
            TextType='ssml'
        )
        return send_file(response.get("AudioStream"), mimetype="audio/mp3", cache_timeout=0)
