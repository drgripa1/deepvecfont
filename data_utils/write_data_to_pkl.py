import argparse
import multiprocessing as mp
import os
import pickle
import numpy as np
import svg_utils

'''
{'uni': int64,  # unicode value of this glyph
'width': int64,  # width of this glyph's viewport (provided by fontforge)
'vwidth': int64,  # vertical width of this glyph's viewport
'sfd': binary/str,  # glyph, converted to .sfd format, with a single SplineSet
'id': binary/str,  # id of this glyph
'binary_fp': binary/str}  # font identifier (provided in glyphazzn_urls.txt)
'''

def create_db(opts):
    print("Process sfd to pkl files ....")
    alphabet_chars = '一丁七万三上下不中久乗九乱乳予事二亡交京人仁仏仕他代以仮件任休会伝似位低住体何余作使例供価便係保修俳俵倉個倍候値停側傷働像億優元兄兆先児党入公六共兵具典内円写冬冷処出刀分刊初判別利制刷券刻則前副割劇力功加助努労効勇勉動勝勤包化北区医十千午卒協南単印危厚原厳去参友反収取受古句史号司合同后向君否吸告周味呼品員唱問喜営器四回因団囲図固国園圧在坂均型域基堂場塩境墓増士声変夏夕外夜夢大天太夫央奏女好妹妻姉委姿婦子存孝季学孫宅宇守完宗官客宣宮害家宿寄密寒寸寺対射将尊導少尺局居届屋属層山岸島川州巣工差己巻布希師帯帰帳常幕平年幹庁広序店府度庫庭康延建弁式弓引弟弱張強当形役往後徒従得復徳心必志忘応忠念思急性恩息悪悲情想意愛感態我戦戸手打批技投折担招拝拡拾持指挙捨授採接推提損操改放救教散敬整敵新方族旗日旧明易昔星映春昨昭時晩晴暖暗暮暴曜曲書最月有望朝期木未末本机材村束条来東松板林枚果枝柱査栄校株格桜梅械棒森植極楽構様模権橋機次欲歌止正武歯歴死残段殺母毎毒比毛氏民気水永池汽河油治沿泉法波泣注泳洋洗活派流浅浴海消液深混清済減温港湯源準演漢潔潮激火灯灰災炭点無然焼熟熱燃父片版牛牧物特犬犯状独率王班球理生産田由申男画界畑留番異疑病痛登白百的皇皮皿益盛目直省看真眼着矢知石砂研破確磁示礼社祖祝票禁福私秋科秒秘程種積穴究空窓立章童競竹笑笛第筆等筋算管節簡米粉精糖糸系紀紅納純紙級素細終組経結給統絶絹綿緑線編練縦縮績織罪置署羊群義翌習老考者耳聖聞肉育肺胃背胸能脈脳腸臓臣臨自至興舌舎船良色花芸芽若苦英荷菜落葉著蒸蔵蚕血衆衛衣表裁裏補製複要見規覚覧親観角計訓記訪設訳証評詞試詩誌認誕語誠誤説読課調談諸謝警議豆象貝負財貧買貸費貿賀賃資賛賞質赤走起足路身車軽輪辞農近返迷退送逆通速造週運過道達遠選郡部郵郷都配酒酸重野金針鉄銀銅銭鏡長閉間関閣防降限陛院除陸険隊際集雪雲青非面革音頂預頭題額顔願類風飛食飯飲飼館駅骨高魚鳥鳴麦黒鼻'
    all_font_ids = sorted(os.listdir(os.path.join(opts.sfd_path, opts.split)))
    num_fonts = len(all_font_ids)
    print(f"Number {opts.split} fonts before processing", num_fonts)
    fonts_per_process = num_fonts // opts.num_processes + 1
    char_num = len(alphabet_chars)

    def process(process_id):
        cur_process_processed_font_glyphs = []
        cur_process_log_file = open(os.path.join(opts.log_dir, f'{opts.split}_log_{process_id}.txt'), 'w')
        cur_process_pkl_file = open(os.path.join(opts.output_path, opts.split, f'{opts.split}_{process_id:04d}-{opts.num_processes+1:04d}.pkl'), 'wb')
        for i in range(process_id * fonts_per_process, (process_id + 1) * fonts_per_process):
            if i >= num_fonts:
                break
            font_id = all_font_ids[i]
            cur_font_sfd_dir = os.path.join(opts.sfd_path, opts.split, font_id)
            cur_font_glyphs = []

            # a whole font as an entry
            for _char in alphabet_chars:
                char_id = ord(_char)
                if not os.path.exists(os.path.join(cur_font_sfd_dir, '{}_{:05d}.sfd'.format(font_id, char_id))):
                    break

                char_desp_f = open(os.path.join(cur_font_sfd_dir, '{}_{:05d}.txt'.format(font_id, char_id)), 'r')
                char_desp = char_desp_f.readlines()
                sfd_f = open(os.path.join(cur_font_sfd_dir, '{}_{:05d}.sfd'.format(font_id, char_id)), 'r')
                sfd = sfd_f.read()

                uni = int(char_desp[0].strip())
                width = int(char_desp[1].strip())
                vwidth = int(char_desp[2].strip())
                char_idx = char_desp[3].strip()
                font_idx = char_desp[4].strip()

                cur_glyph = {}
                cur_glyph['uni'] = uni
                cur_glyph['width'] = width
                cur_glyph['vwidth'] = vwidth
                cur_glyph['sfd'] = sfd
                cur_glyph['id'] = char_idx
                cur_glyph['binary_fp'] = font_idx

                if not svg_utils.is_valid_glyph_wouni(cur_glyph):
                    msg = f"font {font_idx}, char {char_idx} is not a valid glyph\n"
                    cur_process_log_file.write(msg)
                    char_desp_f.close()
                    sfd_f.close()
                    # use the font whose all glyphs are valid
                    break
                pathunibfp = svg_utils.convert_to_path(cur_glyph)

                if not svg_utils.is_valid_path(pathunibfp, max_len=250):
                    msg = f"font {font_idx}, char {char_idx}'s sfd is not a valid path\n"
                    cur_process_log_file.write(msg)
                    char_desp_f.close()
                    sfd_f.close()
                    break

                example = svg_utils.create_example(pathunibfp, max_len=250)

                cur_font_glyphs.append(example)
                char_desp_f.close()
                sfd_f.close()
            
            if len(cur_font_glyphs) == char_num:
                # use the font whose all glyphs are valid
                # merge the whole font
                merged_res = {}
                if not os.path.exists(os.path.join(cur_font_sfd_dir, 'imgs_' + str(opts.img_size) + '.npy')):
                    rendered = np.zeros((char_num, opts.img_size, opts.img_size), np.uint8)
                    rendered_256 = np.zeros((char_num, opts.img_size * 4, opts.img_size * 4), np.uint8)
                    rendered[:, :, :] = 255
                    rendered_256[:, :, :] = 255
                    rendered = rendered.tolist()
                    rendered_256 = rendered_256.tolist()
                else:
                    rendered = np.load(os.path.join(cur_font_sfd_dir, 'imgs_' + str(opts.img_size) + '.npy')).tolist()
                    rendered_256 = np.load(os.path.join(cur_font_sfd_dir, 'imgs_' + str(opts.img_size * 4) + '.npy')).tolist()
                sequence = []
                seq_len = []
                binaryfp = []
                char_class = []
                for char_id in range(char_num):
                    example = cur_font_glyphs[char_id]
                    sequence.append(example['sequence'])
                    seq_len.append(example['seq_len'])
                    char_class.append(example['class'])
                    binaryfp = example['binary_fp']

                merged_res['rendered'] = rendered
                merged_res['rendered_256'] = rendered_256
                merged_res['seq_len'] = seq_len
                merged_res['sequence'] = sequence
                merged_res['class'] = char_class
                merged_res['binary_fp'] = binaryfp
                cur_process_processed_font_glyphs += [merged_res]

        pickle.dump(cur_process_processed_font_glyphs, cur_process_pkl_file)
        cur_process_pkl_file.close()

    processes = [mp.Process(target=process, args=[pid]) for pid in range(opts.num_processes + 1)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("Finished processing all sfd files, logs (invalid glyphs and paths) are saved to", opts.log_dir)


def combine_perprocess_pkl_db(opts):
    print("Combine all pkl files ....")
    all_glyphs = []
    all_glyphs_pkl_file = open(os.path.join(opts.output_path, opts.split, f'{opts.split}_all.pkl'), 'wb')
    for process_id in range(opts.num_processes + 1):
        cur_process_pkl_file = open(os.path.join(opts.output_path, opts.split, f'{opts.split}_{process_id:04d}-{opts.num_processes+1:04d}.pkl'), 'rb')
        cur_process_glyphs = pickle.load(cur_process_pkl_file)
        all_glyphs += cur_process_glyphs
    pickle.dump(all_glyphs, all_glyphs_pkl_file)
    all_glyphs_pkl_file.close()
    return len(all_glyphs)


def cal_mean_stddev(opts):
    print("Calculating all glyphs' mean stddev ....")
    all_fonts_f = open(os.path.join(opts.output_path, opts.split, f'{opts.split}_all.pkl'), 'rb')
    all_fonts = pickle.load(all_fonts_f)
    num_fonts = len(all_fonts)

    fonts_per_process = num_fonts // opts.num_processes
    alphabet_chars = '一丁七万三上下不中久乗九乱乳予事二亡交京人仁仏仕他代以仮件任休会伝似位低住体何余作使例供価便係保修俳俵倉個倍候値停側傷働像億優元兄兆先児党入公六共兵具典内円写冬冷処出刀分刊初判別利制刷券刻則前副割劇力功加助努労効勇勉動勝勤包化北区医十千午卒協南単印危厚原厳去参友反収取受古句史号司合同后向君否吸告周味呼品員唱問喜営器四回因団囲図固国園圧在坂均型域基堂場塩境墓増士声変夏夕外夜夢大天太夫央奏女好妹妻姉委姿婦子存孝季学孫宅宇守完宗官客宣宮害家宿寄密寒寸寺対射将尊導少尺局居届屋属層山岸島川州巣工差己巻布希師帯帰帳常幕平年幹庁広序店府度庫庭康延建弁式弓引弟弱張強当形役往後徒従得復徳心必志忘応忠念思急性恩息悪悲情想意愛感態我戦戸手打批技投折担招拝拡拾持指挙捨授採接推提損操改放救教散敬整敵新方族旗日旧明易昔星映春昨昭時晩晴暖暗暮暴曜曲書最月有望朝期木未末本机材村束条来東松板林枚果枝柱査栄校株格桜梅械棒森植極楽構様模権橋機次欲歌止正武歯歴死残段殺母毎毒比毛氏民気水永池汽河油治沿泉法波泣注泳洋洗活派流浅浴海消液深混清済減温港湯源準演漢潔潮激火灯灰災炭点無然焼熟熱燃父片版牛牧物特犬犯状独率王班球理生産田由申男画界畑留番異疑病痛登白百的皇皮皿益盛目直省看真眼着矢知石砂研破確磁示礼社祖祝票禁福私秋科秒秘程種積穴究空窓立章童競竹笑笛第筆等筋算管節簡米粉精糖糸系紀紅納純紙級素細終組経結給統絶絹綿緑線編練縦縮績織罪置署羊群義翌習老考者耳聖聞肉育肺胃背胸能脈脳腸臓臣臨自至興舌舎船良色花芸芽若苦英荷菜落葉著蒸蔵蚕血衆衛衣表裁裏補製複要見規覚覧親観角計訓記訪設訳証評詞試詩誌認誕語誠誤説読課調談諸謝警議豆象貝負財貧買貸費貿賀賃資賛賞質赤走起足路身車軽輪辞農近返迷退送逆通速造週運過道達遠選郡部郵郷都配酒酸重野金針鉄銀銅銭鏡長閉間関閣防降限陛院除陸険隊際集雪雲青非面革音頂預頭題額顔願類風飛食飯飲飼館駅骨高魚鳥鳴麦黒鼻'
    char_num = len(alphabet_chars)
    manager = mp.Manager()
    return_dict = manager.dict()
    main_stddev_accum = svg_utils.MeanStddev()

    def process(process_id, return_dict):
        mean_stddev_accum = svg_utils.MeanStddev()
        cur_sum_count = mean_stddev_accum.create_accumulator()
        for i in range(process_id * fonts_per_process, (process_id + 1) * fonts_per_process):
            if i >= num_fonts:
                break
            cur_font = all_fonts[i]
            for charid in range(char_num):
                cur_font_char = {}
                cur_font_char['seq_len'] = cur_font['seq_len'][charid]
                cur_font_char['sequence'] = cur_font['sequence'][charid]
                cur_sum_count = mean_stddev_accum.add_input(cur_sum_count, cur_font_char)
        return_dict[process_id] = cur_sum_count
    processes = [mp.Process(target=process, args=[pid, return_dict]) for pid in range(opts.num_processes + 1)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    merged_sum_count = main_stddev_accum.merge_accumulators(return_dict.values())
    output = main_stddev_accum.extract_output(merged_sum_count)
    mean = output['mean']
    stdev = output['stddev']
    mean = np.concatenate((np.zeros([4]), mean[4:]), axis=0)
    stdev = np.concatenate((np.ones([4]), stdev[4:]), axis=0)
    # finally, save the mean and stddev files
    np.save(os.path.join(opts.output_path, opts.split, 'mean'), mean)
    np.save(os.path.join(opts.output_path, opts.split, 'stdev'), stdev)

    # rename npy to npz, to match the file names predefined in main.py
    path_ms = os.path.join(opts.output_path, opts.split)
    os.rename(os.path.join(path_ms, 'mean.npy'), os.path.join(path_ms, 'mean.npz'))
    os.rename(os.path.join(path_ms, 'stdev.npy'), os.path.join(path_ms, 'stdev.npz'))

def main():
    parser = argparse.ArgumentParser(description="LMDB creation")
    # parser.add_argument("--alphabet", type=str, default='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    parser.add_argument("--ttf_path", type=str, default='font_ttfs')
    parser.add_argument('--sfd_path', type=str, default='./font_sfds')
    parser.add_argument("--output_path", type=str, default='../data/vecfont_dataset_/',
                        help="Path to write the database to")
    parser.add_argument('--img_size', type=int, default=64, help="the height and width of glyph images")
    # parser.add_argument('--num_char', type=int, default=52, help="the number of character categories")
    parser.add_argument("--split", type=str, default='train')
    parser.add_argument("--log_dir", type=str, default='./font_sfds/log/')
    parser.add_argument("--num_processes", type=int, default=1, help="number of processes") # the real num will be opts.num_processes + 1
    parser.add_argument("--phase", type=int, default=0, choices=[0, 1, 2, 3],
                        help="0 all, 1 create db, 2 combine_pkl_files, 3 cal stddev")

    opts = parser.parse_args()
    assert os.path.exists(opts.sfd_path), "specified sfd glyphs path does not exist"
    split_path = os.path.join(opts.output_path, opts.split)

    if not os.path.exists(split_path):
        os.makedirs(split_path)

    if not os.path.exists(opts.log_dir):
        os.makedirs(opts.log_dir)

    if opts.phase <= 1:
        create_db(opts)
    
    if opts.phase <= 2:
        number_saved_glyphs = combine_perprocess_pkl_db(opts)
        print(f"Number {opts.split} fonts after processing", number_saved_glyphs)

    if opts.phase <= 3:
        cal_mean_stddev(opts)

    
if __name__ == "__main__":
    main()