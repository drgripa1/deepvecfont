from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fontforge  # noqa
import os
import multiprocessing as mp
import argparse

# conda deactivate
# apt install python3-fontforge

def convert_mp(opts):
    """Useing multiprocessing to convert all fonts to sfd files"""
    alphabet_chars = '一丁七万三上下不中久乗九乱乳予事二亡交京人仁仏仕他代以仮件任休会伝似位低住体何余作使例供価便係保修俳俵倉個倍候値停側傷働像億優元兄兆先児党入公六共兵具典内円写冬冷処出刀分刊初判別利制刷券刻則前副割劇力功加助努労効勇勉動勝勤包化北区医十千午卒協南単印危厚原厳去参友反収取受古句史号司合同后向君否吸告周味呼品員唱問喜営器四回因団囲図固国園圧在坂均型域基堂場塩境墓増士声変夏夕外夜夢大天太夫央奏女好妹妻姉委姿婦子存孝季学孫宅宇守完宗官客宣宮害家宿寄密寒寸寺対射将尊導少尺局居届屋属層山岸島川州巣工差己巻布希師帯帰帳常幕平年幹庁広序店府度庫庭康延建弁式弓引弟弱張強当形役往後徒従得復徳心必志忘応忠念思急性恩息悪悲情想意愛感態我戦戸手打批技投折担招拝拡拾持指挙捨授採接推提損操改放救教散敬整敵新方族旗日旧明易昔星映春昨昭時晩晴暖暗暮暴曜曲書最月有望朝期木未末本机材村束条来東松板林枚果枝柱査栄校株格桜梅械棒森植極楽構様模権橋機次欲歌止正武歯歴死残段殺母毎毒比毛氏民気水永池汽河油治沿泉法波泣注泳洋洗活派流浅浴海消液深混清済減温港湯源準演漢潔潮激火灯灰災炭点無然焼熟熱燃父片版牛牧物特犬犯状独率王班球理生産田由申男画界畑留番異疑病痛登白百的皇皮皿益盛目直省看真眼着矢知石砂研破確磁示礼社祖祝票禁福私秋科秒秘程種積穴究空窓立章童競竹笑笛第筆等筋算管節簡米粉精糖糸系紀紅納純紙級素細終組経結給統絶絹綿緑線編練縦縮績織罪置署羊群義翌習老考者耳聖聞肉育肺胃背胸能脈脳腸臓臣臨自至興舌舎船良色花芸芽若苦英荷菜落葉著蒸蔵蚕血衆衛衣表裁裏補製複要見規覚覧親観角計訓記訪設訳証評詞試詩誌認誕語誠誤説読課調談諸謝警議豆象貝負財貧買貸費貿賀賃資賛賞質赤走起足路身車軽輪辞農近返迷退送逆通速造週運過道達遠選郡部郵郷都配酒酸重野金針鉄銀銅銭鏡長閉間関閣防降限陛院除陸険隊際集雪雲青非面革音頂預頭題額顔願類風飛食飯飲飼館駅骨高魚鳥鳴麦黒鼻'
    alphabet_chars_ids = set(ord(i) for i in alphabet_chars)
    fonts_file_path = opts.ttf_path
    sfd_path = opts.sfd_path
    for root, dirs, files in os.walk(os.path.join(opts.ttf_path, opts.split)):
        ttf_fnames = files
    print(ttf_fnames)
    font_num = len(ttf_fnames)
    # process_nums = mp.cpu_count() - 2
    # if font_num // process_nums < 1:
    #     process_nums = font_num
    #     font_num_per_process = min(font_num // process_nums, 1)
    # else:
    #     font_num_per_process = font_num // process_nums

    # def process(process_id, font_num_p_process):
    #     for i in range(process_id * font_num_p_process, (process_id + 1) * font_num_p_process):
    def process():
        for i in range(font_num):
            # if i >= font_num:
            #     break
            
            font_id = ttf_fnames[i].split('.')[0]
            split = opts.split
            font_name = ttf_fnames[i]
            
            font_file_path = os.path.join(fonts_file_path, split, font_name)
            try:
                cur_font = fontforge.open(font_file_path)
                try:
                    it = cur_font.cidFlatten().glyphs()
                except:
                    it = cur_font.glyphs()
            except Exception as e:
                print('Cannot open', font_name)
                print(e)
                continue

            target_dir = os.path.join(sfd_path, split, "{}".format(font_id))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for glyph in it:
                char_id = glyph.unicode
                if char_id not in alphabet_chars_ids:
                    continue
                char_description = open(os.path.join(target_dir, '{}_{:05d}.txt'.format(font_id, char_id)), 'w')

                cur_font.selection.select(glyph)
                cur_font.copy()

                new_font_for_char = fontforge.font()
                new_font_for_char.encoding = 'UnicodeBMP'
                new_font_for_char.selection.select(char_id, ('unicode',))
                new_font_for_char.paste()
                new_font_for_char.fontname = "{}_".format(font_id) + font_name

                new_font_for_char.save(os.path.join(target_dir, '{}_{:05d}.sfd'.format(font_id, char_id)))

                char_description.write(str(char_id) + '\n')
                char_description.write(str(new_font_for_char[char_id].width) + '\n')
                char_description.write(str(new_font_for_char[char_id].vwidth) + '\n')
                char_description.write('{:05d}'.format(char_id) + '\n')
                char_description.write('{}'.format(font_id))

                char_description.close()

            cur_font.close()

    # processes = [mp.Process(target=process, args=(pid, font_num_per_process)) for pid in range(process_nums + 1)]

    # for p in processes:
    #     p.start()
    # for p in processes:
    #     p.join()
    process()


def main():
    parser = argparse.ArgumentParser(description="Convert ttf fonts to sfd fonts")
    # parser.add_argument("--alphabet", type=str, default='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    parser.add_argument("--ttf_path", type=str, default='font_ttfs')
    parser.add_argument('--sfd_path', type=str, default='font_sfds')
    parser.add_argument('--split', type=str, default='test')
    opts = parser.parse_args()

    convert_mp(opts)


if __name__ == "__main__":
    main()
