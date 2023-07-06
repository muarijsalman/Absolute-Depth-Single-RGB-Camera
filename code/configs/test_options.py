from configs.base_options import BaseOptions

class TestOptions(BaseOptions):
    def initialize(self):
        parser = BaseOptions.initialize(self)
        parser.add_argument('--result_dir', type=str, default='./code/results',
                            help='save result images into result_dir/exp_name')
        parser.add_argument('--ckpt_dir',   type=str,
                            default='./code/ckpt/best_model_nyu.ckpt', 
                            help='load ckpt path')
        
        parser.add_argument('--save_eval_pngs', default=True, action='store_true',
                            help='save result image into evaluation form')
        parser.add_argument('--save_visualize', default=True, action='store_true',
                            help='save result image into visulized form')
        parser.add_argument('--do_evaluate',  default=False,  action='store_true',
                            help='evaluate with inferenced images')        

        
        return parser


