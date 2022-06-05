import re
import torch

from .model import DeepPunctuation, DeepPunctuationCRF
from .config import *

out_str = ''

tokenizer = MODELS['bert-base-multilingual-cased'][1].from_pretrained('bert-base-multilingual-cased')
token_style = MODELS['bert-base-multilingual-cased'][3]

model_save_path = 'D:\\Project with Meeka\\backend\\base\\punctuation_forserver\\weights.pt'
cuda=False

device = torch.device('cuda' if (cuda and torch.cuda.is_available()) else 'cpu')

deep_punctuation = DeepPunctuation('bert-base-multilingual-cased', freeze_bert=False, lstm_dim=-1)
deep_punctuation.to(device)
deep_punctuation.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')), strict=False)
deep_punctuation.eval()

def inference(inp_str):
    # deep_punctuation.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')), strict=False)
    # deep_punctuation.eval()
    text = re.sub(r"[,:\-–.!;?]", '', inp_str)
    words_original_case = text.split()
    words = text.lower().split()

    word_pos = 0
    sequence_len = 256
    result = ""
    decode_idx = 0
    punctuation_map = {0: '', 1: ',', 2: '.', 3: '?'}

    while word_pos < len(words):
        x = [TOKEN_IDX[token_style]['START_SEQ']]
        y_mask = [0]

        while len(x) < sequence_len and word_pos < len(words):
            tokens = tokenizer.tokenize(words[word_pos])
            if len(tokens) + len(x) >= sequence_len:
                break
            else:
                for i in range(len(tokens) - 1):
                    x.append(tokenizer.convert_tokens_to_ids(tokens[i]))
                    y_mask.append(0)
                x.append(tokenizer.convert_tokens_to_ids(tokens[-1]))
                y_mask.append(1)
                word_pos += 1
            
        x.append(TOKEN_IDX[token_style]['END_SEQ'])
        y_mask.append(0)
        if len(x) < sequence_len:
            x = x + [TOKEN_IDX[token_style]['PAD'] for _ in range(sequence_len - len(x))]
            y_mask = y_mask + [0 for _ in range(sequence_len - len(y_mask))]
        attn_mask = [1 if token != TOKEN_IDX[token_style]['PAD'] else 0 for token in x]

        x = torch.tensor(x).reshape(1,-1)
        y_mask = torch.tensor(y_mask)
        attn_mask = torch.tensor(attn_mask).reshape(1,-1)
        x, attn_mask, y_mask = x.to(device), attn_mask.to(device), y_mask.to(device)

        with torch.no_grad():
            y_predict = deep_punctuation(x, attn_mask)
            y_predict = y_predict.view(-1, y_predict.shape[2])
            y_predict = torch.argmax(y_predict, dim=1).view(-1)
        for i in range(y_mask.shape[0]):
            if y_mask[i] == 1:
                result += words_original_case[decode_idx] + punctuation_map[y_predict[i].item()] + ' '
                decode_idx += 1
        print('Punctuated text: {}'.format(result))
        return result
    

if __name__ == '__main__':
  
    #inp_str = input('Enter the sentence: ')
    inference("Мазкур қарорнинг ижросини назорат қилиш шаҳар ҳокимининг қурилиш коммуникациялар коммунал хўжалиги экология ва кўкалмзорлаштириш масалалари бўйича ўринбосари зиммасига юклансин")