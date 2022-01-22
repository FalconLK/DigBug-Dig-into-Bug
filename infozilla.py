import xml.dom.minidom

import os


def main():
    doc = xml.dom.minidom.parse("path/file.xml");
    print(doc.nodeName)
    print(doc.firstChild.tagName)
    expertise = doc.getElementsByTagName("Stacktrace")

    print(len(expertise))
    for skill in expertise:
        print(skill.getAttribute("amount"))

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

if __name__ == "__main__":
    # main()

    import os
    wd = os.getcwd()
    exe_dir = "path"
    os.chdir(exe_dir)

    # put everything in demo/ and loop everything in the demo dir
    # file_lst = []
    # for subdir, dirs, files in os.walk(target_dir + 'demo/'):
    #     for filename in files:
    #         if filename.endswith('gradle'):
    #             continue
    #         # filepath = subdir + os.sep + filename
    #         file_lst.append(filename)

    target_dir = 'path'
    file_lst = files(target_dir)

    for file in file_lst:
        if file.endswith('gradle'):
            continue
        # a = os.popen("/opt/gradle/gradle-6.1/bin/gradle run -s --args='demo/%s'" % file).read()
        a = os.popen("/opt/gradle/gradle-6.1/bin/gradle run -s --args='%s/%s'" % (target_dir, file)).read()
        for line in a.split('\n'):
            if 'Stack' in line:
                if int(line[0]) > 0:
                    print('True')
                else:
                    print('False')


    # a = os.popen("/opt/gradle/gradle-6.1/bin/gradle run --args='demo/demo.txt'").read()
    print('----------')
    # print(a)
    os.chdir(wd)

    # works for gradle
    # os.system("/opt/gradle/gradle-6.1/bin/gradle run --args='demo/demo.txt'")

    # doesn't work for gradle
    # subprocess.Popen("/opt/gradle/gradle-6.1/bin/gradle run")
    # subprocess.Popen("gradle run --args='demo/demo.txt'")
    # subprocess.Popen("ls")

    # doesn't work for gradle
    # proc = subprocess.Popen(["/opt/gradle/gradle-6.1/bin/gradle", "run", "--args='demo/demo.txt"],
    #                         stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    # print("program output:", out)
