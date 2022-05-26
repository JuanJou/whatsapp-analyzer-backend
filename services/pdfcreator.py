from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def create_pdf():
    year = [2014, 2015, 2016, 2017, 2018, 2019]  
    tutorial_count = [39, 117, 111, 110, 67, 29]

    plt.plot(year, tutorial_count, color="#6c3376", linewidth=3)  
    plt.xlabel('Year')  
    plt.ylabel('Number of futurestud.io Tutorials')
    plt.savefig("plot.pdf")
    return open("plot.pdf", mode="rb")
