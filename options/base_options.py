import argparse
import os
from util import util
import pickle


class BaseOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
        self.parser.add_argument('--dataroot', required=True, help='path to images (should have subfolders trainA, trainB, valA, valB, etc)')
        self.parser.add_argument('--batchSize', type=int, default=2, help='input batch size')
        self.parser.add_argument('--loadSize', type=int, default=286, help='scale images to this size')
        self.parser.add_argument('--fineSize', type=int, default=256, help='then crop to this size')
        self.parser.add_argument('--input_nc', type=int, default=3, help='# of input image channels')
        self.parser.add_argument('--output_nc', type=int, default=3, help='# of output image channels')
        self.parser.add_argument('--nz', type=int, default=8, help='#latent vector')
        self.parser.add_argument('--nef', type=int, default=64, help='# of encoder filters in first conv layer')
        self.parser.add_argument('--ngf', type=int, default=64, help='# of gen filters in first conv layer')
        self.parser.add_argument('--ndf', type=int, default=64, help='# of discrim filters in first conv layer')

        self.parser.add_argument('--gpu_ids', type=str, default='0', help='gpu ids: e.g. 0  0,1,2, 0,2, -1 for CPU mode')
        self.parser.add_argument('--name', type=str, default='experiment_name', help='name of the experiment. It decides where to store samples and models')
        self.parser.add_argument('--resize_or_crop', type=str, default='resize_and_crop', help='not implemented')
        self.parser.add_argument('--dataset_mode', type=str, default='aligned', help='aligned,single')
        self.parser.add_argument('--model', type=str, default='bicycle_gan', help='chooses which model to use. bicycle,, ...')
        self.parser.add_argument('--which_direction', type=str, default='AtoB', help='AtoB or BtoA')
        self.parser.add_argument('--nThreads', default=4, type=int, help='# sthreads for loading data')
        self.parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints', help='models are saved here')

        self.parser.add_argument('--serial_batches', action='store_true', help='if true, takes images in order to make batches, otherwise takes them randomly')
        self.parser.add_argument('--display_winsize', type=int, default=256,  help='display window size')
        self.parser.add_argument('--display_id', type=int, default=1, help='window id of the web display')
        self.parser.add_argument('--display_port', type=int, default=8000,  help='visdom display port')
        self.parser.add_argument('--use_dropout', action='store_true', help='use dropout for the generator')
        self.parser.add_argument('--max_dataset_size', type=int, default=float("inf"), help='Maximum number of samples allowed per dataset. If the dataset directory contains more than max_dataset_size, only a subset is loaded.')
        self.parser.add_argument('--no_flip', action='store_true', help='if specified, do not flip the images for data argumentation')

        # models
        self.parser.add_argument('--num_Ds', type=int, default=2, help='number of Discrminators')
        self.parser.add_argument('--gan_mode', type=str, default='lsgan', help='dcgan|lsgan')
        self.parser.add_argument('--which_model_netD', type=str, default='basic_256_multi', help='selects model to use for netD')
        self.parser.add_argument('--which_model_netD2', type=str, default='basic_256_multi', help='selects model to use for netD')
        self.parser.add_argument('--which_model_netG', type=str, default='unet_256', help='selects model to use for netG')
        self.parser.add_argument('--which_model_netE', type=str, default='resnet_256', help='selects model to use for netE')
        self.parser.add_argument('--norm', type=str, default='instance', help='instance normalization or batch normalization')
        self.parser.add_argument('--upsample', type=str, default='basic', help='basic | bilinear')
        self.parser.add_argument('--nl', type=str, default='relu', help='non-linearity activation: relu | lrelu | elu')

        # extra parameters
        self.parser.add_argument('--where_add', type=str, default='all', help='input|all|middle; where to add z in the network G')
        self.parser.add_argument('--conditional_D', action='store_true', help='if use conditional GAN for D')
        self.parser.add_argument('--init_type', type=str, default='xavier', help='network initialization [normal|xavier|kaiming|orthogonal]')
        self.parser.add_argument('--center_crop', action='store_true', help='if apply for center cropping for the test')
        # special tasks
        self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        self.opt.isTrain = self.isTrain   # train or test

        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)

        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        if self.isTrain:
            expr_dir = os.path.join(self.opt.checkpoints_dir, self.opt.name)
            util.mkdirs(expr_dir)
            pkl_file = os.path.join(expr_dir, 'opt.pkl')
            pickle.dump(self.opt, open(pkl_file, 'wb'))

            # save to the disk
            file_name = os.path.join(expr_dir, 'opt_train.txt')
            with open(file_name, 'wt') as opt_file:
                opt_file.write('------------ Options -------------\n')
                for k, v in sorted(args.items()):
                    opt_file.write('%s: %s\n' % (str(k), str(v)))
                opt_file.write('-------------- End ----------------\n')
        else:
            results_dir = self.opt.results_dir
            util.mkdirs(results_dir)
        return self.opt
