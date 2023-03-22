import json
from flask import Flask, render_template, request

from pycocotools.coco import COCO

app = Flask(__name__,template_folder='templates')

def get_imgInfo(coco_id):
    coco_annotation_file_path = "/projects/stpa9007/Image_Caption_Viewer/annotations/instances_val2014.json"

    coco_annotation = COCO(annotation_file=coco_annotation_file_path)

    img_ids = coco_annotation.getImgIds()

    img_info = coco_annotation.loadImgs(img_ids)

    info = {}

    for im in img_info:
        if im['id'] == coco_id:
            info = im


    return info

    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the image ID from the form data
    coco_id = request.form['image_id']

    # Search for the image ID in the captions JSON file
    
    # Get the image URL using the COCO API

    # Load the JSON files
    with open('/projects/stpa9007/Image_Caption_Viewer/coco/caption_results_coco.json') as f:
        captions = json.load(f)
    with open('/projects/stpa9007/Image_Caption_Viewer/coco/id2captions_test_coco.json') as f:
        gt_captions = json.load(f)

    # for img in images:
    #     if img['cocoid'] == int(coco_id):
    #         filename = img['filename']

    # img = images[int(image_id)]
    # cocoid = img['cocoid']    
    

    img_info = get_imgInfo(int(coco_id))
    #base_url = "http://images.cocodataset.org/val2014/"
    image_url = img_info['coco_url']
    #image_url = base_url + filename

    if str(coco_id) in gt_captions:
        original_1 = gt_captions[str(coco_id)][0]
        original_2 = gt_captions[str(coco_id)][1]
        original_3 = gt_captions[str(coco_id)][2]
        original_4 = gt_captions[str(coco_id)][3]
        original_5 = gt_captions[str(coco_id)][4]

    print(image_url)
 
    if image_url !="":
        # Get the four captions for the image ID
        caption_1 = captions["1"][str(coco_id)][0]
        caption_2 = captions["2"][str(coco_id)][0]
        caption_3 = captions["3"][str(coco_id)][0]
        caption_4 = captions["4"][str(coco_id)][0]

        # Render the template with the image URL and captions
        return render_template('search.html', image_url=image_url,
                               caption_1=caption_1['caption'], caption_2=caption_2['caption'],
                               caption_3=caption_3['caption'], caption_4=caption_4['caption'], original_1 = original_1,
                               original_2 = original_2, original_3 = original_3, original_4 = original_4, original_5 = original_5)
    else:
        # If the image ID is not found, render an error message
        return render_template('error.html', message='Image not found')

if __name__ == '__main__':
    app.run(debug=True)
