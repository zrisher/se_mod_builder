import shutil


def gen_example_project_config(global_config, target_dir):
    template_path = global_config['install_dir'] + '\\build.example.yml'
    dst_path = target_dir + '\\build.yml'
    print('Generating project config at "{}" from template at "{}"'
          .format(dst_path, template_path))
    shutil.copy2(template_path, dst_path)
