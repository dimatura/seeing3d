
# This is a example script to export files using Sketchup's ruby scripting.
# Therefore you have to run it from inside ruby. (I just use the console).
# btw: I am not a ruby programmer!
# Also: I haven't tried this in a long time, so you may have to change for
# newer sketchup versions.

require 'sketchup.rb'

OUT_DIR = "f:\\curated0_exported"

#INPUT_DIR = "c:\\Users\\dmaturan\\Downloads\\chair2"
INPUT_DIR = "f:\\curated0"

Dir.chdir(INPUT_DIR)

#img_id = 0
#skp_fnames = Dir.glob("*.skp")

skp_fnames = ["f:\\curated0_models\\35ee4bcad88ab50af6e44a01c524295b.skp",
"f:\\curated0_models\\375eb8b8515084b5518b6fc7ed4f3487.skp",
"f:\\curated0_models\\b4c73f4772efcf69742728b30848ed03.skp",
"f:\\curated0_models\\b4ed57bca8ddf9ebada15d23c9da81e3.skp",
"f:\\curated0_models\\c33a0e02f295c69835836c728d324152.skp",
"f:\\curated0_models\\ce24e17dfd60ead335836c728d324152.skp",
"f:\\curated0_models\\dd7165d82e2f5f00a2a0c56253e2ad78.skp",
"f:\\curated0_models\\fa85fc5c2f223fed35836c728d324152.skp"]

skp_fnames.each { |skp_fname|
    base_fname = skp_fname[0..-5]
    Sketchup.open_file(skp_fname)
    model = Sketchup.active_model
    options_hash = { 
        :triangulated_faces   => true,
        :doublesided_faces    => false,
        :edges                => false,
        :materials_by_layer   => false,
        :author_attribution   => false,
        :texture_maps         => true,
        :selectionset_only    => false,
        :preserve_instancing  => false,
        :preserve_hierarchy   => false
    }
    # for DAE
    status = model.export(base_fname+'.dae', options_hash)
    puts skp_fname + '->' + base_fname + ' .. ' + status.to_s
}

Dir.chdir("..")
file_loaded("export_dae.rb")
