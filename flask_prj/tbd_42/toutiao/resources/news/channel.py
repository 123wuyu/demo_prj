from flask_restful import Resource

from cache import channel as cache_channel


class ChannelListResource(Resource):
    """
    频道列表
    """
    def get(self):
        """
        获取所有频道信息
        """
        ret = cache_channel.AllChannelsCache.get()
        return {'channels': ret}
