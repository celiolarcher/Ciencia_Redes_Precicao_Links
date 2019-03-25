import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import weka.core.Instances;
import weka.core.Option;
import weka.attributeSelection.ClassifierAttributeEval;
import weka.classifiers.trees.J48;
import java.util.Enumeration;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Collection;

public class execute{
	public static class AttributeScore implements Comparable<AttributeScore>{
		public String attributeName;
		public double score;

		public AttributeScore(String name, double score){
			this.attributeName=name;
			this.score=score;
		}

		public int compareTo(AttributeScore attr2){
		   Double score1=this.score;
		   Double score2=attr2.score;

		   return -score1.compareTo(score2);
		}
	};

	public static void main(String args[]){
		String[] listFiles={"../Bases/gc_data.arff"};//{"../Bases/newmovies.arff"};//../Bases/GNP.arff","../Bases/SmallWorld.arff","../Bases/PreferentialAttachment.arff"};
		try{
			for(String file: listFiles){
		 		BufferedReader reader = new BufferedReader(new FileReader(file));
			
				Instances data = new Instances(reader);
				reader.close();

				data.setClassIndex(data.numAttributes() - 1);
	

				ClassifierAttributeEval evaluation = new ClassifierAttributeEval();

//				for(String s:evaluation.getOptions())	
//					System.out.println(s);
				
				List <AttributeScore> listAttr=new ArrayList<AttributeScore>();

				String[] listClassifiers={".SMO",".NaiveBayes",".J48",".RandomForest"};
				for(String classifier:listClassifiers){

//					String optionTest[] = {"-L","-E","auc","-B",classifier};
					String optionTest[] = {"-E","auc","-B",classifier};
					evaluation.setOptions(optionTest);

//					for(String s:evaluation.getOptions())	
//						System.out.println(s);

			
					evaluation.buildEvaluator(data);


					System.out.println(classifier+" done");					
					System.out.println("Sumary:");

					
					for(int i=0; i<data.numAttributes()-1;i++){
						AttributeScore attr=new AttributeScore(data.attribute(i).name(),evaluation.evaluateAttribute(i));
						listAttr.add(attr);
					}

					Collections.sort(listAttr);

					for(AttributeScore attr:listAttr){
						System.out.println(attr.attributeName+"\t"+attr.score);
					}

					listAttr.clear();					
				}

								
				System.out.println("Analyze in "+file+" done.");
			}
		}catch(IOException e){
			System.out.println("Arquivo não encontrado \n");
		}catch(Exception e){
			System.out.println("Erro classificador \n");
		}
	}
}
