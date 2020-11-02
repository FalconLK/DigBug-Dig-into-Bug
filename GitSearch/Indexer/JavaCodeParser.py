#!/usr/bin/env python
# -*- coding: utf-8 -*-

from JavaASTVisitor import JavaASTVisitor
from CommentASTVisitor import CommentASTVisitor
from org.eclipse.jdt.core.dom import ASTParser, AST, ASTNode
from java.lang import String

from java.util.concurrent import Callable
from java.lang import Runnable


from org.eclipse.jface.text import Document
from org.eclipse.jdt.core.dom.rewrite import ASTRewrite
import csv

def rename_processor(methodToRename):
	from org.eclipse.jdt.internal.corext.refactoring.rename import JavaRenameProcessor

	processor = RenameVirtualMethodProcessor(methodToRename)
	processor.setUpdateReferences(True);
	processor.setNewElementName("newMethodName");

	fRefactoring = RenameRefactoring(processor);
	fChange= fRefactoring.createChange(NullProgressMonitor());
	fChange.initializeValidationData(NullProgressMonitor());
	fChange.perform(NullProgressMonitor())

def clean_ast(nodes):
	is_not_thing = lambda x: x not in ["JDTCrazyType", "JDTAugmentedClass", "JDTAugmentedMethod"]
	nodes["used_classes"] = filter(is_not_thing, nodes["used_classes"])
	nodes["returns"] = filter(is_not_thing, nodes["returns"])
	nodes["classes"] = filter(is_not_thing, nodes["classes"])
	nodes["methods"] = filter(is_not_thing, nodes["methods"])

	return nodes


def parse(sourceCodeString, with_ln=True, resolve=False):
	
	source = sourceCodeString

	node = setupASTParser(source, resolve)
	
	v = JavaASTVisitor(node) if with_ln else JavaASTVisitor()



	

	# theClass = node.types()[0]
	# className = theClass.getName()
	# className.setIdentifier("MyOwnClass")
	# theClass.setName(node.getAST().newSimpleName("bar1"))

	# methods = theClass.getMethods()
	# for method in methods:
	# 	method.setName(ast.newSimpleName("MyCoolMethod"))
	# 	print method.getName()

	# print ast.toString()

	# print node.toString()
	#modifyAST(node)

	
	if not node:
		return v.AST

	#if node.getAST().hasBindingsRecovery():
	#	print("Binding activated.")
	
	# print node.getFlags()
	# if node.getFlags() == ASTNode.MALFORMED:
	# 	print "Malformed"
	# elif node.getFlags() == ASTNode.ORIGINAL:
	# 	print "Original"
	# elif node.getFlags() == ASTNode.PROTECT:
	# 	print "Protect"
	# elif node.getFlags() == ASTNode.RECOVERED:
	# 	print "Recovered"

	# if the parsed node gets some error, it means the source code is not CompilationUnit
	# try enclosing the code with class and method
	if node.getFlags() > ASTNode.ORIGINAL:
		source = "class JDTAugmentedClass{\n JDTCrazyType JDTAugmentedMethod(){\n" + sourceCodeString +"\n}\n}";
		node = setupASTParser(source, resolve);
		

	if not node:
		return v.AST



	if node.getFlags() > ASTNode.ORIGINAL:
		
		source = "class JDTAugmentedClass{" + sourceCodeString +"}";
		node = setupASTParser(source, resolve);
		print "Class AUgmented"
		
	if not node:
		return v.AST

	try:
		node.accept(v);
	except:
		print "Error in accept"
		return v.AST


	# c = CommentASTVisitor(node, source)
	# for comment in node.getCommentList():
	# 	comment.accept(c)
	
	# v.AST["comments"] = c.comments
	#print clean_ast(v.AST)

	#print node.toString()
	return clean_ast(v.get_AST())


def new_parser(source_string):
	parser = setupASTParser(source_string, True)
	cu = parser.createAST(None)



def setupASTParser(sourceCodeString, resolve, parser_type=ASTParser.K_COMPILATION_UNIT):
	parser = ASTParser.newParser(AST.JLS4)
	parser.setSource(String(sourceCodeString).toCharArray())
	parser.setResolveBindings(resolve)
	parser.setStatementsRecovery(resolve)
	parser.setBindingsRecovery(resolve)
	parser.setEnvironment(["/Users/Raphael/Google Drive/GitSearchScala/out/production/"], None, None, True)
	parser.setUnitName("JDTAugmentedClass.class")
	parser.setKind(parser_type)

	
	try:
		node = parser.createAST(None)
	except:
		print("Error: %s" %(sourceCodeString))
		node = None
		
	return node

class JDTParser(Callable, Runnable):
	def __init__(self, source, doc, callback):
		self.source = source
		self.callback = callback
		self.doc = doc
		self.result = None

	def call(self):
		self.result = self.callback(self.source)
		return self

	def run(self):
		self.result = self.callback(self.source)
		return self

if __name__ == '__main__':

	# import time

	# start = time.time()
	

	# with open('/Users/Raphael/Downloads/code-sample.csv', 'r') as csvfile:
	# 	spamreader = csv.reader(csvfile)
	# 	for row in spamreader:
	# 		parse(row[3])

	# end = time.time()
	# print end - start

	source = """ 
		class A{void stub() { IWorkspaceRoot root = ResourcesPlugin.getWorkspace().getRoot(); IProject project = root.getProject(\"someJavaProject\"); project.open(null /* IProgressMonitor */); IJavaProject javaProject = JavaCore.create(project);}}
	"""
	source = "String.valueOf(i)"
	#source = 'StringBuilder sb = new StringBuilder(); sb.append("tmp"); sb.append("b"); String l = sb.toString();'
	#source = 'java.awt.Desktop.getDesktop().browse(new URI("http://stackoverflow.com"));'
	source1 = "Matcher.find()"
	source = "MySuperSpecialType.go()"
	source = "class JDTAugmentedClass{ JDTCrazyType JDTAugmentedMethod(){JarFile.entries();}}"
	source4 = """ 
				public boolean visit(MethodInvocation node) {
				    Expression exp = node.getExpression();
				    ITypeBinding typeBinding = node.getExpression().resolveTypeBinding();
				    System.out.println("Type: " + typeBinding.toString());
				    String s = StrangeClass.valueOf(3);
				    String s = instance.valueOf(3);
				}

			 """
	source5 = 	"""
					BufferedImage myPicture = ImageIO.read(new File("path-to-file"));
					JLabel picLabel = new JLabel(new ImageIcon(myPicture));
					add(picLabel);
					
				"""

	source = """
			import java.awt.Graphics;
			import java.awt.image.BufferedImage;
			import java.io.File;
			import java.io.IOException;
			import java.util.logging.Level;
			import java.util.logging.Logger;
			import javax.imageio.ImageIO;
			import javax.swing.JPanel;

			public class ImagePanel extends JPanel{

			    private BufferedImage image;

			    public ImagePanel() {
			       try {                
			          image = ImageIO.read(new File("image name and path"));
			       } catch (IOException ex) {
			            // handle exception...
			       }
			    }

			    @Override
			    protected void paintComponent(Graphics g) {
			        super.paintComponent(g);
			        g.drawImage(image, 0, 0, null); // see javadoc for more info on the parameters            
			    }

			}
	"""

	source = """
			package hiyoko;
 
			import java.awt.Color;
			import java.awt.Graphics;
			 
			import javax.swing.JPanel;
			 
			public class HiyokoPanel extends JPanel {
			 
				HiyokoPanel(){
					super();
				}
			 
				public void paintComponent(Graphics g){
					super.paintComponent(g);
			 		System.out.println("Hallo");
					g.setColor(Color.white);
					g.fillRect(0, 0, this.getWidth(), this.getHeight());
				}
			 
			}
	"""

	

	source = """ URL url = Resources.getResource("foo.txt");
String text = Resources.toString(url, Charsets.UTF_8);"""

	source =""" for (String line : Files.readAllLines(Paths.get("/path/to/file.txt"))) {
		    // ...
		}"""
	
	source = """ 
		enum StringCompressor {
    ;
    public static byte[] compress(String text) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            OutputStream out = new DeflaterOutputStream(baos);
            out.write(text.getBytes("UTF-8"));
            out.close();
        } catch (IOException e) {
            throw new AssertionError(e);
        }
        return baos.toByteArray();
    }

    public static String decompress(byte[] bytes) {
        InputStream in = new InflaterInputStream(new ByteArrayInputStream(bytes));
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            byte[] buffer = new byte[8192];
            int len;
            while((len = in.read(buffer))>0)
                baos.write(buffer, 0, len);
            return new String(baos.toByteArray(), "UTF-8");
        } catch (IOException e) {
            throw new AssertionError(e);
        }
    }
}
	"""

	source = """
		public class Testing {

		    public static void main(String[] args) {

		        HashMap<String,Double> map = new HashMap<String,Double>();
		        ValueComparator bvc =  new ValueComparator(map);
		        TreeMap<String,Double> sorted_map = new TreeMap<String,Double>(bvc);

		        map.put("A",99.5);
		        map.put("B",67.4);
		        map.put("C",67.4);
		        map.put("D",67.3);

		        System.out.println("unsorted map: "+map);

		        sorted_map.putAll(map);

		        System.out.println("results: "+sorted_map);
		    }
		}

		class ValueComparator implements Comparator<String> {

		    Map<String, Double> base;
		    public ValueComparator(Map<String, Double> base) {
		        this.base = base;
		    }

		    // Note: this comparator imposes orderings that are inconsistent with equals.    
		    public int compare(String tmp, String b) {
		        if (base.get(tmp) >= base.get(b)) {
		            return -1;
		        } else {
		            return 1;
		        } // returning 0 would merge keys
		    }
		}
	"""

	

	


		
	source = """JSONObject obj = new JSONObject("{interests : [{interestKey:Dogs}, {interestKey:Cats}]}");

List<String> list = new ArrayList<String>();
JSONArray array = obj.getJSONArray("interests");
for(int i = 0 ; i < array.length() ; i++){
    list.add(array.getJSONObject(i).getString("interestKey"));
}"""



	source = """ 
		URL website = new URL("http://www.website.com/information.asp");
ReadableByteChannel rbc = Channels.newChannel(website.openStream());
FileOutputStream fos = new FileOutputStream("information.html");
fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
	"""

	source = """ 
		class A{
    public static byte[] compress(String text) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            OutputStream out = new DeflaterOutputStream(baos);
            out.write(text.getBytes("UTF-8"));
            out.close();
        } catch (IOException e) {
            throw new AssertionError(e);
        }
        return baos.toByteArray();
    }

    public static String decompress(byte[] bytes) {
        InputStream in = new InflaterInputStream(new ByteArrayInputStream(bytes));
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            byte[] buffer = new byte[8192];
            int len;
            while((len = in.read(buffer))>0)
                baos.write(buffer, 0, len);
            return new String(baos.toByteArray(), "UTF-8");
        } catch (IOException e) {
            throw new AssertionError(e);
        }
    }
}
	"""

	source = """ 
	ContentResolver cr = getContentResolver();
    Cursor cur = cr.query(ContactsContract.Contacts.CONTENT_URI,
        null, null, null, null);
    while (cur.moveToNext()) {
        try{
            String lookupKey = cur.getString(cur.getColumnIndex(
                ContactsContract.Contacts.LOOKUP_KEY));
            Uri uri = Uri.withAppendedPath(ContactsContract.
                Contacts.CONTENT_LOOKUP_URI, lookupKey);
            System.out.println("The uri is " + uri.toString());
            cr.delete(uri, null, null);
        }
    catch(Exception e)
    {
        System.out.println(e.getStackTrace());
    }
}
	"""

	source = """ 
	package com.example.android.apis.view;

// Need the following import to get access to the app resources, since this
// class is in tmp sub-package.
import com.example.android.apis.R;

import android.app.Activity;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Chronometer;

public class ChronometerDemo extends Activity {
    Chronometer mChronometer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.chronometer);

        Button button;

        mChronometer = (Chronometer) findViewById(R.id.chronometer);

        // Watch for button clicks.
        button = (Button) findViewById(R.id.start);
        button.setOnClickListener(mStartListener);

        button = (Button) findViewById(R.id.stop);
        button.setOnClickListener(mStopListener);

        button = (Button) findViewById(R.id.reset);
        button.setOnClickListener(mResetListener);

        button = (Button) findViewById(R.id.set_format);
        button.setOnClickListener(mSetFormatListener);

        button = (Button) findViewById(R.id.clear_format);
        button.setOnClickListener(mClearFormatListener);
    }

    View.OnClickListener mStartListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.start();
        }
    };

    View.OnClickListener mStopListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.stop();
        }
    };

    View.OnClickListener mResetListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
        }
    };

    View.OnClickListener mSetFormatListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setFormat("Formatted time (%s)");
        }
    };

    View.OnClickListener mClearFormatListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setFormat(null);
        }
    };
}

	"""
	source1 = """
	/*
 * Copyright (C) 2007 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain tmp copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.android.apis.view;

// Need the following import to get access to the app resources, since this
// class is in tmp sub-package.
import com.example.android.apis.R;

import android.app.Activity;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Chronometer;

public class ChronometerDemo extends Activity {
    Chronometer mChronometer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.chronometer);

        Button button;

        mChronometer = (Chronometer) findViewById(R.id.chronometer);

        // Watch for button clicks.
        button = (Button) findViewById(R.id.start);
        button.setOnClickListener(mStartListener);

        button = (Button) findViewById(R.id.stop);
        button.setOnClickListener(mStopListener);

        button = (Button) findViewById(R.id.reset);
        button.setOnClickListener(mResetListener);

        button = (Button) findViewById(R.id.set_format);
        button.setOnClickListener(mSetFormatListener);

        button = (Button) findViewById(R.id.clear_format);
        button.setOnClickListener(mClearFormatListener);
    }

    View.OnClickListener mStartListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.start();
        }
    };

    View.OnClickListener mStopListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.stop();
        }
    };

    View.OnClickListener mResetListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
        }
    };

    View.OnClickListener mSetFormatListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setFormat("Formatted time (%s)");
        }
    };

    View.OnClickListener mClearFormatListener = new OnClickListener() {
        public void onClick(View v) {
            mChronometer.setFormat(null);
        }
    };
}

	"""

	# source = """
	# public FirstPanel() {

 #    History.addHistoryListener(this);
 #    String token = History.getToken();
 #    if (token.length() == 0) {
 #        History.newItem(INIT_STATE);
 #    } else {
 #        History.fireCurrentHistoryState();
 #    }

 #    .. rest of code """

 	source2 = """View.OnClickListener mStartButtonListener = new OnClickListener() {
        @Override
        public void onClick(View arg0) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
            mChronometer.start();
        }
    }; """

# 	source = """
# 		String status = Environment.getExternalStorageState();
# if(status.equals("mounted")){
#    String path = your path;
# }

# recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
# recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
# recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
# recorder.setOutputFile(path);
# recorder.prepare();
# recorder.start();
#     """
	

	source1 = """ 
	package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.ViewGroup;
import android.widget.FrameLayout;

public class ActionBarContainer extends FrameLayout {
    private boolean mIsTransitioning;

    public ActionBarContainer(Context context) {
        this(context, null);
    }

    public ActionBarContainer(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        return mIsTransitioning || super.onInterceptTouchEvent(ev);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        super.onTouchEvent(event);
        return true;
    }

    public void setTransitioning(boolean transitioning) {
        mIsTransitioning = transitioning;
        setDescendantFocusability(transitioning ? ViewGroup.FOCUS_BLOCK_DESCENDANTS : ViewGroup.FOCUS_AFTER_DESCENDANTS);
    }
}
"""

	source2 = """ 
	  public void onItemSelected(AdapterView<?> listView, View view, int position, long id)
{
    if (position == 1)
    {
        // listView.setItemsCanFocus(true);

        // Use afterDescendants, because I don't want the ListView to steal focus
        listView.setDescendantFocusability(ViewGroup.FOCUS_AFTER_DESCENDANTS);
        myEditText.requestFocus();
    }
    else
    {
        if (!listView.isFocused())
        {
            // listView.setItemsCanFocus(false);

            // Use beforeDescendants so that the EditText doesn't re-take focus
            listView.setDescendantFocusability(ViewGroup.FOCUS_BEFORE_DESCENDANTS);
            listView.requestFocus();
        }
    }
}

public void onNothingSelected(AdapterView<?> listView)
{
    // This happens when you start scrolling, so we need to prevent it from staying
    // in the afterDescendants mode if the EditText was focused 
    listView.setDescendantFocusability(ViewGroup.FOCUS_BEFORE_DESCENDANTS);
}
	"""

	source = """
	long seed = System.nanoTime();
Collections.shuffle(fileList, new Random(seed));
Collections.shuffle(imgList, new Random(seed));
	"""

	ast = parse(source, resolve=True)
	print ast
	# print "FQN"

	# class_fqn_map = { im.split(".")[-1]: im for im in ast["imports"] }
	# print class_fqn_map
	# print "Used_classes", ast["used_classes"]

	# fqnm_list = []
	# method_fqn_type_map = {}
	# # In case we match tmp typed_method_call
	# for tmc in ast["typed_method_call"]:
	# 	class_name, method_name = tmc.split(".")
	# 	if class_name in class_fqn_map:
	# 		print tmc, tmc.replace(class_name, class_fqn_map[class_name], 1)

	# 		fqnm = tmc.replace(class_name, class_fqn_map[class_name], 1) # Replace only first occurrence
	# 		fqnm_list.append( fqnm ) 

	# 		method_fqn_type_map[method_name] = {}
	# 		method_fqn_type_map[method_name]["fqn"] = fqnm
	# 		method_fqn_type_map[method_name]["class"] = class_fqn_map[class_name]

	# print "method_fqn_type_map", method_fqn_type_map
	# # Case we match only tmp method_call 1. determine FQNM 2. assign variable name to FQN


	# print ast

	# print "----"*10

	# ast = parse(source2, resolve=True)

	# # convert partial qualified named variables to fully qualified names
	# for var, var_type in ast["var_type_map"].iteritems():
	# 	# In case PQN is prefixed by some identifier
	# 	if "." in var_type:
	# 		parts = var_type.split(".")
	# 		# Get Suffix
	# 		suffixed_var_type = parts[-1]
	# 		prefixed_var_type = parts[0]
	# 		if suffixed_var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[suffixed_var_type]
	# 		elif prefixed_var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[prefixed_var_type] + "." + ".".join(parts[1:])
	# 	else:
	# 		if var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[var_type]
			
	# 	if var not in ast["var_type_map"]:
	# 		print "Could not resolve: %s, %s" %  (var_type ,var)



	# # Resolved untyped variables
	# for umc in ast["unresolved_method_calls"]:
	# 	unresolved_var, method_name = umc.split(".")

	# 	print unresolved_var, method_fqn_type_map[method_name]["class"]

	# 	ast["var_type_map"][unresolved_var] = method_fqn_type_map[method_name]["class"]

	# # Resolve untyped method calls
	# for method_name in ast["methods_called"]:
	# 	print method_fqn_type_map[method_name]["fqn"]

	
	# print ast

	


	# 