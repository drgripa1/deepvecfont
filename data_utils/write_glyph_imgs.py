from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import argparse
import numpy as np
import os

def write_glyph_imgs(opts):
    alphabet_chars = '一丁七万三上下不中久乗九乱乳予事二亡交京人仁仏仕他代以仮件任休会伝似位低住体何余作使例供価便係保修俳俵倉個倍候値停側傷働像億優元兄兆先児党入公六共兵具典内円写冬冷処出刀分刊初判別利制刷券刻則前副割劇力功加助努労効勇勉動勝勤包化北区医十千午卒協南単印危厚原厳去参友反収取受古句史号司合同后向君否吸告周味呼品員唱問喜営器四回因団囲図固国園圧在坂均型域基堂場塩境墓増士声変夏夕外夜夢大天太夫央奏女好妹妻姉委姿婦子存孝季学孫宅宇守完宗官客宣宮害家宿寄密寒寸寺対射将尊導少尺局居届屋属層山岸島川州巣工差己巻布希師帯帰帳常幕平年幹庁広序店府度庫庭康延建弁式弓引弟弱張強当形役往後徒従得復徳心必志忘応忠念思急性恩息悪悲情想意愛感態我戦戸手打批技投折担招拝拡拾持指挙捨授採接推提損操改放救教散敬整敵新方族旗日旧明易昔星映春昨昭時晩晴暖暗暮暴曜曲書最月有望朝期木未末本机材村束条来東松板林枚果枝柱査栄校株格桜梅械棒森植極楽構様模権橋機次欲歌止正武歯歴死残段殺母毎毒比毛氏民気水永池汽河油治沿泉法波泣注泳洋洗活派流浅浴海消液深混清済減温港湯源準演漢潔潮激火灯灰災炭点無然焼熟熱燃父片版牛牧物特犬犯状独率王班球理生産田由申男画界畑留番異疑病痛登白百的皇皮皿益盛目直省看真眼着矢知石砂研破確磁示礼社祖祝票禁福私秋科秒秘程種積穴究空窓立章童競竹笑笛第筆等筋算管節簡米粉精糖糸系紀紅納純紙級素細終組経結給統絶絹綿緑線編練縦縮績織罪置署羊群義翌習老考者耳聖聞肉育肺胃背胸能脈脳腸臓臣臨自至興舌舎船良色花芸芽若苦英荷菜落葉著蒸蔵蚕血衆衛衣表裁裏補製複要見規覚覧親観角計訓記訪設訳証評詞試詩誌認誕語誠誤説読課調談諸謝警議豆象貝負財貧買貸費貿賀賃資賛賞質赤走起足路身車軽輪辞農近返迷退送逆通速造週運過道達遠選郡部郵郷都配酒酸重野金針鉄銀銅銭鏡長閉間関閣防降限陛院除陸険隊際集雪雲青非面革音頂預頭題額顔願類風飛食飯飲飼館駅骨高魚鳥鳴麦黒鼻'

    for root, dirs, files in os.walk(os.path.join(opts.ttf_path, opts.split)):
        ttf_names = files
    ttf_names.sort()
    for fontid in range(len(ttf_names)):
        fontname = ttf_names[fontid].split('.')[0]
        print(fontname)
        g_idx_dict = {}
        ttf_file_path = os.path.join(opts.ttf_path, opts.split, ttf_names[fontid])

        try:
            font = ImageFont.truetype(ttf_file_path, opts.img_size, encoding="unic")
        except:
            print('cant open ' + fontname)
            continue

        fontimgs_array = np.zeros((len(alphabet_chars), opts.img_size, opts.img_size), np.uint8)
        fontimgs_array[:, :, :] = 255

        for idx, char in enumerate(alphabet_chars):
            charid = ord(char)
            # read the meta file
            txt_fpath = os.path.join(opts.sfd_path, opts.split, fontname, fontname + '_' + "%05d"%(charid) + '.txt')
            try:
                txt_lines = open(txt_fpath,'r').read().split('\n')
            except:
                print('cannot read text file')
                continue

            # the offsets are calculated according to the rules in data_utils/svg_utils.py
            vbox_w = float(txt_lines[1])
            vbox_h = float(txt_lines[2])
            norm = max(int(vbox_w), int(vbox_h))

            if int(vbox_h) > int(vbox_w):
                add_to_y = 0
                add_to_x = abs(int(vbox_h) - int(vbox_w)) / 2
                add_to_x = add_to_x * (float(opts.img_size) / norm)
            else:
                add_to_y = abs(int(vbox_h) - int(vbox_w)) / 2
                add_to_y = add_to_y * (float(opts.img_size) / norm)
                add_to_x = 0

            # char = opts.alphabet[charid]
            array = np.ndarray((opts.img_size,opts.img_size), np.uint8)
            array[:, :] = 255
            image = Image.fromarray(array)
            draw = ImageDraw.Draw(image)

            try:
                font_width, font_height = font.getsize(char)
            except:
                print('cant calculate height and width ' + "%s"%fontname + '_' + "%05d"%(charid))
                continue
            
            try:
                ascent, descent = font.getmetrics()
            except:
                print('cannot get ascent, descent')
                continue

            # delta = (opts.img_size - (descent + ascent)) /2
            # draw.text((add_to_x, add_to_y + opts.img_size-ascent-int((opts.img_size/24.0)*(4.0/3.0))), char, (0) ,font=font)
            d = 0
            if ascent > opts.img_size:
                if opts.img_size == 256:
                    d = 50
                elif opts.img_size == 64:
                    d = 14
            draw.text((add_to_x, add_to_y - d), char, (0) ,font=font)
            fontimgs_array[idx] = np.array(image)

        # os.makedirs(os.path.join(opts.sfd_path, 'im_debug'), exist_ok=True)
        # image.save(os.path.join(opts.sfd_path, 'im_debug', f'{fontname}_{charid}_{opts.img_size}.png'))
            
        np.save(os.path.join(opts.sfd_path, opts.split, fontname, 'imgs_' + str(opts.img_size) + '.npy'), fontimgs_array)

def main():
    parser = argparse.ArgumentParser(description="Write glyph images")
    # parser.add_argument("--alphabet", type=str, default='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    parser.add_argument("--ttf_path", type=str, default='font_ttfs')
    parser.add_argument('--sfd_path', type=str, default='font_sfds')
    parser.add_argument('--img_size', type=int, default=64)
    parser.add_argument('--split', type=str, default='train')
    opts = parser.parse_args()

    write_glyph_imgs(opts)


if __name__ == "__main__":
    main()

