from docx import Document
from docxcompose.composer import Composer
from docx import Document as Document_compose
from docxtpl import DocxTemplate
class WordTool:
    def combine_word_documents(self, files):
        merged_document = Document()

        try:
            for index, file in enumerate(files):
                sub_doc = Document(file)

                # Don't add a page break if you've reached the last file.
                if index < len(files)-1:
                    sub_doc.add_page_break()

                for element in sub_doc.element.body:
                    merged_document.element.body.append(element)

            merged_document.save('merged.docx')

        except Exception as e:
            print(f"Error combining Word documents: {e}")
            
    def combined(self, filename_master , filename_second_docx):
        
        #filename_master is name of the file to merge the docx file into
        master = Document_compose(filename_master)

        composer = Composer(master)
        #filename_second_docx is the name of the second docx file
        doc2 = Document_compose(filename_second_docx)
        # append the doc2 into the master using composer.append function
        composer.append(doc2)
        #Save the combined docx with a name
        composer.save("combined.docx")
        
    def set_cover(self, docx_template_path,  replacements_dict, output_path= 'modified_document.docx'):
        """
        Replace placeholders in a DOCX template file with values from the dictionary using docxtpl.

        Parameters:
        - docx_template_path (str): Path to the input DOCX template file.
        - output_path (str): Path to save the modified DOCX file.
        - replacements_dict (dict): Dictionary containing placeholders and their corresponding values.

        Example:
        - replacements_dict = {'title': 'New Title', 'author': 'John Doe'}
        - set_cover('input_template.docx', 'modified_document.docx', replacements_dict)
        """
        doc = DocxTemplate(docx_template_path)

        # Use the render method to replace placeholders with values
        context = replacements_dict
        doc.render(context)

        # Save the modified document
        doc.save(output_path)