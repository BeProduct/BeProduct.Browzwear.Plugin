import BwApi
import urllib.request
import urllib.parse
import urllib
import config
import os
import json
from .remote_asset_library import RemoteAssetLibrary

def __get_content__(url):
    response = urllib.request.urlopen(url, context=config.SSL_CONTEXT)
    return response.read().decode('utf-8')
    
class BeProduct3DDevelopmentAssets(BwApi.CallbackBase):
    library = None 
    colors = None
    def Run(self, garmentId, callbackId, dataString):
        ind = 0
        path_components = os.path.normpath(BwApi.GarmentPathGet(garmentId)).split(os.sep)
        if path_components[-1].lower().endswith('.bw'):
            ind=1
        if len(path_components) > 6:

            # materials from 3d development app
            i = ind - 1
            filename = "%2F".join(map(urllib.parse.quote,path_components[:i if i != 0 else None]))
            if BeProduct3DDevelopmentAssets.library is not None \
                and BeProduct3DDevelopmentAssets.library.library is not None \
                and BeProduct3DDevelopmentAssets.library.library.library_id:

                BwApi.AssetLibRemove(BeProduct3DDevelopmentAssets.library.library.library_id)
            libs = json.loads(__get_content__(config.BASE_URL + "api/bw/getfilelibraries?f=" + filename))
            for lib in libs:
                BeProduct3DDevelopmentAssets.library = RemoteAssetLibrary(lib)
                BeProduct3DDevelopmentAssets.library.initialize()


            # colors for 3d development app 
            colors_json = __get_content__(config.BASE_URL + "api/bw/colors?f=" + filename)
            BeProduct3DDevelopmentAssets.colors = BwApi.ColorLibraryCreate(garmentId, colors_json)

          

        return 0