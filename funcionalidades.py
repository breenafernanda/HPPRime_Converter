import fitz
import zipfile
import shutil
import os
import io
from tkinter import messagebox
from PIL import Image, ImageTk

def pdf_to_hp_prime(pdf_path):
    base_name = os.path.basename(pdf_path)[:8].replace(" ", "_")
    new_zip_name = f"{base_name}.zip"
    new_hpprgm_name = f"{base_name}.hpprgm"
    new_hpappdir_zip_name = f"{base_name}.hpappdir.zip"
    new_hpappdir_internal_name = f"{base_name}.hpappdir"

    # Caminho do arquivo zip padrão e novo caminho para o zip renomeado
    default_zip_path = "arquivo_hp.zip"
    current_dir = os.getcwd()
    new_zip_path = os.path.join(current_dir, new_zip_name)

    # Copia o arquivo zip padrão para um novo arquivo zip com o nome do PDF
    shutil.copy(default_zip_path, new_zip_path)

    # Inicialmente com 3 arquivos padrão + número de páginas do PDF
    pdf_document = fitz.open(pdf_path)
    num_files = 3 + len(pdf_document)
    pdf_document.close()

    # Atualizar conteudo de applist.txt
    applist_content = f"** applist.txt\n  2097152 : max supported app size\n  1305611                     {num_files} files\n\t{new_hpappdir_internal_name}\n"
    print("Conteúdo atualizado de applist.txt:")
    print(applist_content)

    # Atualizar conteudo de arquivo_hp.hpprgm
    hpprgm_content = f"""#pragma mode( separator(.,;) integer(h64) )
LOCAL baseappname="{base_name}";
LOCAL pggroup=20;
LOCAL pgmax=15;
mynum2str(n,r) BEGIN
 LOCAL s="",i=1+FLOOR(LOG(r));
 WHILE n>0 DO
  s:=CHAR(ASC("0")+(n MOD 10))+s;
  n:=IP(n/10);
 END;
 WHILE DIM(s)<i DO s:="0"+s; END;
 RETURN s;
END;

range(a,b) BEGIN
 IF a≠b THEN
  RETURN mynum2str(a,pgmax)+"_"+mynum2str(b,pgmax);
 ELSE
  RETURN mynum2str(a,pgmax);
 END;
END;
EXPORT {base_name}()
BEGIN
 LOCAL appname=baseappname;
 IF pgmax>pggroup THEN
  appname:=appname+" "+range(1,pggroup);
 END;
 STARTAPP(appname);
END;"""
    print("Conteúdo atualizado de arquivo_hp.hpprgm:")
    print(hpprgm_content)

    # Abre o novo arquivo zip para edição
    with zipfile.ZipFile(new_zip_path, 'r') as zipf:
        with zipfile.ZipFile("temp.zip", 'w') as temp_zip:
            for item in zipf.infolist():
                data = zipf.read(item.filename)
                if item.filename == "arquivo_hp.hpprgm":
                    temp_zip.writestr(new_hpprgm_name, hpprgm_content)
                elif item.filename == "arquivo_hp.hpappdir.zip":
                    with zipfile.ZipFile(io.BytesIO(data), 'r') as hpappdir_zip:
                        with zipfile.ZipFile("temp_hpappdir.zip", 'w') as temp_hpappdir_zip:
                            for hpappdir_item in hpappdir_zip.infolist():
                                hpappdir_data = hpappdir_zip.read(hpappdir_item.filename)
                                if hpappdir_item.filename == "arquivo_hp.hpappdir/arquivo_hp.hpapp":
                                    temp_hpappdir_zip.writestr(f"{new_hpappdir_internal_name}/{base_name}.hpapp", hpappdir_data)
                                elif hpappdir_item.filename == "arquivo_hp.hpappdir/arquivo_hp.hpappnote":
                                    temp_hpappdir_zip.writestr(f"{new_hpappdir_internal_name}/{base_name}.hpappnote", hpappdir_data)
                                elif hpappdir_item.filename == "arquivo_hp.hpappdir/arquivo_hp.hpappprgm":
                                    temp_hpappdir_zip.writestr(f"{new_hpappdir_internal_name}/{base_name}.hpappprgm", hpappdir_data)
                                elif hpappdir_item.filename == "arquivo_hp.hpappdir/":
                                    # Adiciona as imagens do PDF
                                    pdf_document = fitz.open(pdf_path)
                                    for page_num in range(len(pdf_document)):
                                        page = pdf_document.load_page(page_num)
                                        pix = page.get_pixmap()
                                        img_bytes = pix.tobytes("png")
                                        temp_hpappdir_zip.writestr(f"{new_hpappdir_internal_name}/{page_num + 1:02d}.png", img_bytes)
                                    pdf_document.close()
                                else:
                                    temp_hpappdir_zip.writestr(hpappdir_item.filename.replace("arquivo_hp.hpappdir", new_hpappdir_internal_name), hpappdir_data)
                    with open("temp_hpappdir.zip", "rb") as temp_hpappdir_zip_file:
                        temp_zip.writestr(new_hpappdir_zip_name, temp_hpappdir_zip_file.read())
                elif item.filename == "applist.txt":
                    temp_zip.writestr(item.filename, applist_content)
                else:
                    temp_zip.writestr(item.filename, data)

    shutil.move("temp.zip", new_zip_path)
    messagebox.showinfo("Sucesso", f"Arquivo HP Prime criado: {new_zip_path}")

    # Apagar o arquivo temp_hpappdir.zip da pasta
    if os.path.exists("temp_hpappdir.zip"):
        os.remove("temp_hpappdir.zip")

def display_pdf(pdf_path, label, page_number):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img = img.resize((400, 500), Image.LANCZOS)  # Ajustar o tamanho da imagem para caber na janela
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img
    pdf_document.close()
