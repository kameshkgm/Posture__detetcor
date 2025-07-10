from configobj import ConfigObj
import numpy as np

def config_reader():
    try:
        config = ConfigObj('config')

        if 'param' not in config or 'models' not in config:
            raise ValueError("Missing [param] or [models] section in config file.")

        param = config['param']
        model_id = str(param.get('modelID'))
        if model_id not in config['models']:
            raise ValueError(f"Model ID '{model_id}' not found in [models] section.")

        model = config['models'][model_id]

        # Basic int/float casting
        model['boxsize'] = int(model.get('boxsize', 368))
        model['stride'] = int(model.get('stride', 8))
        model['padValue'] = int(model.get('padValue', 128))

        # Handle part_str properly
        if 'part_str' in model:
            model['part_str'] = [s.strip().strip('"') for s in model['part_str']]

        param['octave'] = int(param.get('octave', 3))
        param['use_gpu'] = int(param.get('use_gpu', 0))
        param['starting_range'] = float(str(param.get('starting_range')).split('#')[0].strip())
        param['ending_range'] = float(str(param.get('ending_range')).split('#')[0].strip())

        # 🔧 FIX: Parse scale_search properly
        scale_str = str(param.get('scale_search')).split('#')[0].strip()
        param['scale_search'] = [float(x.strip()) for x in scale_str.split(',') if x.strip()]

        param['thre1'] = float(param.get('thre1', 0.1))
        param['thre2'] = float(param.get('thre2', 0.05))
        param['thre3'] = float(param.get('thre3', 0.5))
        param['mid_num'] = int(param.get('mid_num', 10))
        param['min_num'] = int(param.get('min_num', 4))
        param['crop_ratio'] = float(param.get('crop_ratio', 0.4))
        param['bbox_ratio'] = float(param.get('bbox_ratio', 0.25))
        param['GPUdeviceNumber'] = int(param.get('GPUdeviceNumber', 0))

        print("✅ Config loaded successfully")
        print("scale_search:", param['scale_search'])
        print("part_str:", model['part_str'])

        return param, model

    except Exception as e:
        print("❌ Error in config_reader():", str(e))
        raise

if __name__ == "__main__":
    config_reader()
