import logging
import json
from flask import request, Flask
from g4f import debug, version, models
from g4f import _all_models, get_last_provider, ChatCompletion
from g4f.Provider import __providers__
from g4f.Provider.bing.create_images import patch_provider
from .internet import get_search_message

debug.logging = True

class Backend_Api:
    def __init__(self, app: Flask) -> None:
        self.app: Flask = app
        self.routes = {
            '/backend-api/v2/models': {
                'function': self.models,
                'methods' : ['GET']
            },
            '/backend-api/v2/providers': {
                'function': self.providers,
                'methods' : ['GET']
            },
            '/backend-api/v2/version': {
                'function': self.version,
                'methods' : ['GET']
            },
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            },
            '/backend-api/v2/gen.set.summarize:title': {
                'function': self._gen_title,
                'methods': ['POST']
            },
            '/backend-api/v2/error': {
                'function': self.error,
                'methods': ['POST']
            }
        }
    
    def error(self):
        print(request.json)
        
        return 'ok', 200
    
    def models(self):
        return _all_models
    
    def providers(self):
        return [
            provider.__name__ for provider in __providers__ if provider.working
        ]
        
    def version(self):
        return {
            "version": version.utils.current_version,
            "lastet_version": version.utils.latest_version,
        }
    
    def _gen_title(self):
        return {
            'title': ''
        }
    
    def _conversation(self):
        #jailbreak = request.json['jailbreak']
        messages = request.json['meta']['content']['parts']
        if request.json.get('internet_access'):
            messages[-1]["content"] = get_search_message(messages[-1]["content"])
        model = request.json.get('model')
        model = model if model else models.default
        provider = request.json.get('provider', '').replace('g4f.Provider.', '')
        provider = provider if provider and provider != "Auto" else None
        patch = patch_provider if request.json.get('patch_provider') else None

        def try_response():
            try:
                first = True
                for chunk in ChatCompletion.create(
                    model=model,
                    provider=provider,
                    messages=messages,
                    stream=True,
                    ignore_stream_and_auth=True,
                    patch_provider=patch
                ):
                    if first:
                        first = False
                        yield json.dumps({
                            'type'    : 'provider',
                            'provider': get_last_provider(True)
                        }) + "\n"
                    yield json.dumps({
                        'type'   : 'content',
                        'content': chunk,
                    }) + "\n"
                
            except Exception as e:
                logging.exception(e)
                yield json.dumps({
                    'type' : 'error',
                    'error': f'{e.__class__.__name__}: {e}'
                })

        return self.app.response_class(try_response(), mimetype='text/event-stream')