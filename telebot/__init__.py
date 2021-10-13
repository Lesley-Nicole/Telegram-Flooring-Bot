'''start action server'''
'''docker run -p 5055:5055 --mount type=bind,source=<absolute_path_to_actions>,target=/app/actions \ '''
'''rasa/rasa-sdk:<version>'''

'''action server at http://localhost:5055/webhook'''