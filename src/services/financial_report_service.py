import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.io.formats.style import Styler

def generate_report(data, report_type="csv", columns=None, title="Report", visualize=False):
    """
    Gelen veriyi belirli bir formatta rapor olarak döndüren jenerik bir fonksiyon.

    :param data: Raporu oluşturmak için kullanılacak ham veriler (DataFrame, list of lists, vs.).
    :param report_type: Raporun döndürüleceği format (örn. "csv", "xlsx", "json").
    :param columns: Raporu oluşturacak sütun isimleri (eğer veri seti sütun isimlerini içermiyorsa).
    :param title: Raporun başlığı.
    :param visualize: Veri görselleştirme seçeneği. True ise, bir grafik oluşturur.
    :return: Raporun döndürüldüğü dosyanın adı veya dosyanın kendisi.
    """
    # Verinin pandas DataFrame'e dönüştürülmesi
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data, columns=columns)

    # Görselleştirme ops
    if visualize:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=data)
        plt.title(f"{title} Visualization")
        plt.savefig(f"{title.replace(' ', '_')}_visualization.png")

    # DataFrame'in belirli bir formatta rapor dosyasına dönüştürülmesi
    report_filename = f"{title.replace(' ', '_')}.{report_type}"
    if report_type == "csv":
        data.to_csv(report_filename, index=False)
    elif report_type == "xlsx":
        with pd.ExcelWriter(report_filename) as writer:
            data.to_excel(writer, index=False, sheet_name='Data')
            # if visualize:
            #     writer.sheets['Data'].insert_image('G1', f"{title.replace(' ', '_')}_visualization.png")
    elif report_type == "json":
        data.to_json(report_filename, orient='records')
    else:
        raise ValueError("Unsupported report type provided.")

    return report_filename

# Örnek veri ve rapor oluşturma işlemi
sample_data = [[1, 'Product A', 100], [2, 'Product B', 150], [3, 'Product C', 200]]
columns = ['ID', 'Product Name', 'Sales']
report_name = generate_report(sample_data, report_type="xlsx", columns=columns, title="Sales Report", visualize=True)

print(f"Generated report: {report_name}")