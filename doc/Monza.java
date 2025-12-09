import java.util.Random;
import java.util.Scanner;

/**
 * Jeu de société "Monza" où le but est d'atteindre la dernière case le premier
 * 
 * @author niels
 *
 */

public class Monza {
	/**
	 * Type aggrégé pour créer une case
	 * 
	 * @author niels
	 *
	 */

	static class Case {

		/**
		 * Couleur de la case
		 */
		String couleur;
		/**
		 * Est-ce que la case est la dernière case de la ligne, condition de victoire
		 */
		boolean estDerniere;
		/**
		 * Pour définir la case suivante
		 */
		Case caseSuivante;
		/**
		 * Pour définir la case en dessous, s'il y'en a une
		 */
		Case caseDessous;
		/**
		 * Pour définir la case au dessus, s'il y'en a une
		 */
		Case caseDessus;
		/**
		 * Pour définir la case précédente
		 */
		Case casePrecedente;

		/**
		 * Definition des paramètres à utiliser pour créer une case
		 * 
		 * @param couleur
		 * @param estDerniere
		 * @param ligne
		 */
		public Case(String couleur, boolean estDerniere) {

			this.couleur = couleur;
			this.estDerniere = estDerniere;
		}

	}

	/**
	 * Type aggrégé pour créer un bolide
	 * 
	 * @author niels
	 *
	 */
	static class Bolide {
		/**
		 * "Couleur" du bolide, B1 ou B2 en l'occurence
		 */
		String couleurB;
		/**
		 * Case occupée par le bolide
		 */
		Case caseOccupee;
		/**
		 * Ligne occupée par le bolide
		 */
		int ligne;
		/**
		 * Pour changer de bolide au changement de tour
		 */
		Bolide next;
		/**
		 * Nom du bolide
		 */
		String nom;

		/**
		 * Definition des paramètres à utiliser pour créer un bolide
		 * 
		 * @param couleur
		 * @param caseOccupee
		 * @param ligne
		 */
		public Bolide(String couleur, Case caseOccupee, int ligne, String nom) {

			this.couleurB = couleur;
			this.caseOccupee = caseOccupee;
			this.ligne = ligne;
			this.nom = nom;
		}

	}

	/**
	 * Choix aléatoire d'une couleur, le dé
	 * 
	 * @return
	 */
	static String randomCouleur() {
		String[] couleurs = { "ROUG", "VERT", "JAUN", "BLEU", "ROSE", "BLAN" };
		Random random = new Random();
		String couleurCible = couleurs[random.nextInt(couleurs.length)];
		return couleurCible;

	}

	/**
	 * Affichage du circuit évoluant suivant la partie
	 * 
	 * @param caseDep11
	 * @param caseDep21
	 * @param bolide
	 */
	static void afficheCircuit(Case caseDep11, Case caseDep21, Bolide bolide) {
		Case c1 = caseDep11;
		Case c2 = caseDep21;
		System.out.println(" __________________________________________");
		if ((bolide.caseOccupee == c1 || bolide.caseOccupee == c2)
				&& (bolide.next.caseOccupee == c1 || bolide.next.caseOccupee == c2)) {
			while (c1 != null) {
				System.out.print(" | " + c1.couleur);
				c1 = c1.caseSuivante;
			}
			System.out.println(" |");
			System.out.println(" __________________________________________");
			while (c2 != null) {
				System.out.print(" | " + c2.couleur);
				c2 = c2.caseSuivante;
			}
			System.out.println(" |");
			System.out.println(" __________________________________________");
		} else {
			while (c1 != null) {
				if (c1 == bolide.caseOccupee) {
					System.out.print(" | " + bolide.couleurB);
				} else if (c1 == bolide.next.caseOccupee) {
					System.out.print(" | " + bolide.next.couleurB);
				} else {
					System.out.print(" | " + c1.couleur);
				}
				c1 = c1.caseSuivante;
			}
			System.out.println(" |");
			System.out.println(" __________________________________________");
			while (c2 != null) {
				if (c2 == bolide.caseOccupee) {
					System.out.print(" | " + bolide.couleurB);
				} else if (c1 == bolide.next.caseOccupee) {
					System.out.print(" | " + bolide.next.couleurB);
				} else {
					System.out.print(" | " + c2.couleur);
				}
				c2 = c2.caseSuivante;
			}
			System.out.println(" |");
			System.out.println(" __________________________________________");
		}

	}

	/**
	 * Création des cases puis reliage entres-elles Création des bolides Premier
	 * lancé de dés Algorithme pour détecter la ligne du bolide, détection des
	 * couleurs puis mouvement du bolide et affichage
	 * 
	 * @param args
	 */
	public static void main(String[] args) {

		Case caseDep11 = new Case("DEP", false);
		Case caseBleu11 = new Case("BLEU", false);
		Case caseRouge11 = new Case("ROUG", false);
		Case caseVert11 = new Case("VERT", false);
		Case caseBleu12 = new Case("BLEU", false);
		Case caseJaune11 = new Case("JAUN", true);

		caseDep11.caseSuivante = caseBleu11;
		caseBleu11.caseSuivante = caseRouge11;
		caseRouge11.caseSuivante = caseVert11;
		caseVert11.caseSuivante = caseBleu12;
		caseBleu12.caseSuivante = caseJaune11;

		Case caseDep21 = new Case("DEP", false);
		Case caseRose21 = new Case("ROSE", false);
		Case caseJaune21 = new Case("JAUN", false);
		Case caseBlanc21 = new Case("BLAN", false);
		Case caseRouge21 = new Case("ROUG", false);
		Case caseVert21 = new Case("VERT", true);

		caseDep21.caseSuivante = caseRose21;
		caseRose21.caseSuivante = caseJaune21;
		caseJaune21.caseSuivante = caseBlanc21;
		caseBlanc21.caseSuivante = caseRouge21;
		caseRouge21.caseSuivante = caseVert21;

		caseDep11.caseDessous = caseDep21;
		caseBleu11.caseDessous = caseRose21;
		caseRouge11.caseDessous = caseJaune21;
		caseVert11.caseDessous = caseBlanc21;
		caseBleu12.caseDessous = caseRouge21;
		caseJaune11.caseDessous = caseVert21;

		caseDep21.caseDessus = caseDep11;
		caseRose21.caseDessus = caseBleu11;
		caseJaune21.caseDessus = caseRouge11;
		caseBlanc21.caseDessus = caseVert11;
		caseRouge21.caseDessus = caseBleu12;
		caseVert21.caseDessus = caseJaune11;

		caseBleu11.casePrecedente = caseDep11;
		caseRouge11.casePrecedente = caseBleu11;
		caseVert11.casePrecedente = caseRouge11;
		caseBleu12.casePrecedente = caseVert11;

		caseRose21.casePrecedente = caseDep21;
		caseJaune21.casePrecedente = caseRose21;
		caseBlanc21.casePrecedente = caseJaune21;
		caseRouge21.casePrecedente = caseBlanc21;

		Bolide bolide = new Bolide("XOOX", caseDep11, 1, "");
		Bolide B1 = new Bolide("XB1X", caseDep11, 1, "B1");
		Bolide B2 = new Bolide("XB2X", caseDep21, 2, "B2");
		B1.next = B2;
		B2.next = B1;

		Scanner scanner = new Scanner(System.in);
		bolide = B1;
		afficheCircuit(caseDep11, caseDep21, bolide);
		String couleur1 = randomCouleur();
		String couleur2 = randomCouleur();
		String couleur3 = randomCouleur();
		System.out.println("C'est au tour de " + bolide.nom + ". Il lance les dés");
		System.out.println(bolide.nom + " obtient les couleurs " + couleur1 + ", " + couleur2 + ", " + couleur3);
		while (!bolide.caseOccupee.estDerniere) {
			while ((bolide.ligne == 1) && (bolide.caseOccupee.caseSuivante.caseDessous.couleur != couleur1
					&& bolide.caseOccupee.caseSuivante.caseDessous.couleur != couleur2
					&& bolide.caseOccupee.caseSuivante.caseDessous.couleur != couleur3
					&& bolide.caseOccupee.caseSuivante.couleur != couleur1
					&& bolide.caseOccupee.caseSuivante.couleur != couleur2
					&& bolide.caseOccupee.caseSuivante.couleur != couleur3)) {
				couleur1 = randomCouleur();
				couleur2 = randomCouleur();
				couleur3 = randomCouleur();
				bolide = bolide.next;
				System.out.println("C'est au tour de " + bolide.nom + ". Il lance les dés");
				System.out
						.println(bolide.nom + " obtient les couleurs " + couleur1 + ", " + couleur2 + ", " + couleur3);
			}

			if ((bolide.ligne == 1)
					&& (bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur1
							|| bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur2
							|| bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur3)
					&& (bolide.caseOccupee.caseSuivante.couleur == couleur1
							|| bolide.caseOccupee.caseSuivante.couleur == couleur2
							|| bolide.caseOccupee.caseSuivante.couleur == couleur3)) {
				System.out.println("Le bolide peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("1 - Passer en haut");
				System.out.println("2 - Passer en bas");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 1 && userInput != 2) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (userInput == 1) {
					if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante) {
						bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
					}
					bolide.caseOccupee = bolide.caseOccupee.caseSuivante;
					afficheCircuit(caseDep11, caseDep21, bolide);
				} else {
					if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante) {
						bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
					}
					bolide.caseOccupee = bolide.caseOccupee.caseSuivante.caseDessous;
					bolide.ligne = 2;
					afficheCircuit(caseDep11, caseDep21, bolide);
				}
			} else if ((bolide.ligne == 1) && (bolide.caseOccupee.caseSuivante.couleur == couleur1
					|| bolide.caseOccupee.caseSuivante.couleur == couleur2
					|| bolide.caseOccupee.caseSuivante.couleur == couleur3)) {
				System.out.println("Le bolide peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("1 - Passer en haut");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 1) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante) {
					bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
				}
				bolide.caseOccupee = bolide.caseOccupee.caseSuivante;
				afficheCircuit(caseDep11, caseDep21, bolide);
			} else if ((bolide.ligne == 1) && (bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur1
					|| bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur2
					|| bolide.caseOccupee.caseSuivante.caseDessous.couleur == couleur3)) {
				System.out.println("Le bolide peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("2 - Passer en bas");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 2) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante.caseDessous) {
					bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
				}
				bolide.caseOccupee = bolide.caseOccupee.caseSuivante.caseDessous;
				bolide.ligne = 2;
				afficheCircuit(caseDep11, caseDep21, bolide);
			}
			while ((bolide.ligne == 2) && (bolide.caseOccupee.caseSuivante.caseDessus.couleur != couleur1
					&& bolide.caseOccupee.caseSuivante.caseDessus.couleur != couleur2
					&& bolide.caseOccupee.caseSuivante.caseDessus.couleur != couleur3
					&& bolide.caseOccupee.caseSuivante.couleur != couleur1
					&& bolide.caseOccupee.caseSuivante.couleur != couleur2
					&& bolide.caseOccupee.caseSuivante.couleur != couleur3)) {
				couleur1 = randomCouleur();
				couleur2 = randomCouleur();
				couleur3 = randomCouleur();
				bolide = bolide.next;
				System.out.println("C'est au tour de " + bolide.nom + ". Il lance les dés");
				System.out
						.println(bolide.nom + " obtient les couleurs " + couleur1 + ", " + couleur2 + ", " + couleur3);
			}
			if ((bolide.ligne == 2)
					&& (bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur1
							|| bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur2
							|| bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur3)
					&& (bolide.caseOccupee.caseSuivante.couleur == couleur1
							|| bolide.caseOccupee.caseSuivante.couleur == couleur2
							|| bolide.caseOccupee.caseSuivante.couleur == couleur3)) {
				System.out.println(bolide.nom + " peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("1 - Passer en haut");
				System.out.println("2 - Passer en bas");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 1 && userInput != 2) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (userInput == 1) {
					if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante.caseDessus) {
						bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
					}
					bolide.caseOccupee = bolide.caseOccupee.caseSuivante.caseDessus;
					bolide.ligne = 1;
					afficheCircuit(caseDep11, caseDep21, bolide);
				} else {
					if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante) {
						bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
					}
					bolide.caseOccupee = bolide.caseOccupee.caseSuivante;
					afficheCircuit(caseDep11, caseDep21, bolide);
				}
			} else if ((bolide.ligne == 2) && (bolide.caseOccupee.caseSuivante.couleur == couleur1
					|| bolide.caseOccupee.caseSuivante.couleur == couleur2
					|| bolide.caseOccupee.caseSuivante.couleur == couleur3)) {
				System.out.println("Le bolide peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("2 - Passer en bas");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 2) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante) {
					bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
				}
				bolide.caseOccupee = bolide.caseOccupee.caseSuivante;
				afficheCircuit(caseDep11, caseDep21, bolide);
			} else if ((bolide.ligne == 2) && (bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur1
					|| bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur2
					|| bolide.caseOccupee.caseSuivante.caseDessus.couleur == couleur3)) {
				System.out.println("Le bolide peut avancer");
				System.out.println("Choix possibles : ");
				System.out.println("1 - Passer en haut");
				System.out.println("Que choississez vous ? ");
				int userInput = scanner.nextInt();
				while (userInput != 1) {
					System.out.println("Erreur : Que choississez vous ? ");
					userInput = scanner.nextInt();
				}
				if (bolide.next.caseOccupee == bolide.caseOccupee.caseSuivante.caseDessus) {
					bolide.next.caseOccupee = bolide.next.caseOccupee.casePrecedente;
				}
				bolide.caseOccupee = bolide.caseOccupee.caseSuivante.caseDessus;
				bolide.ligne = 1;
				afficheCircuit(caseDep11, caseDep21, bolide);
			}
			if (bolide.caseOccupee.couleur == couleur1) {
				couleur1 = "";
			} else if (bolide.caseOccupee.couleur == couleur2) {
				couleur2 = "";
			} else if (bolide.caseOccupee.couleur == couleur3) {
				couleur3 = "";
			}
			if (couleur1 == "" && couleur2 == "") {
				System.out.println("Couleur restante : " + couleur3);
			} else if (couleur1 == "" && couleur3 == "") {
				System.out.println("Couleur restante : " + couleur2);
			} else if (couleur2 == "" && couleur3 == "") {
				System.out.println("Couleur restante : " + couleur1);
			} else if (couleur1 == "") {
				System.out.println("Couleur restantes : " + couleur2 + ", " + couleur3);
			} else if (couleur2 == "") {
				System.out.println("Couleur restantes : " + couleur1 + ", " + couleur3);
			} else if (couleur3 == "") {
				System.out.println("Couleur restantes : " + couleur1 + ", " + couleur2);
			}
		}
		System.out.println(bolide.nom + " a gagné !");
		scanner.close();
	}

}