#include <iostream>
#include <cassert>
#include <cmath>   // for sqrt, fabs
#include <cfloat>  // for DBL_MAX
#include <cstdlib> // for rand, srand
#include <ctime>   // for rand seed
#include <fstream>
#include <cstdio> // for EOF
#include <string>
#include <algorithm> // for count
#include <vector>


struct point
{
	static int d;
	double *coords;
	int label;

	point()
	{
		coords = new double[d];
		label = 0;
		for (int i = 0; i < d; i++)
			coords[i] = 0.0;
	}

	~point()
	{
		delete[] coords;
	}

	void print()
	{
		std::cout << coords[0];
		for (int i = 1; i < d; i++)
			std::cout << "\t" << coords[i];
		std::cout << std::endl;
	}

	double dist(point &q)
	{
		double sqd = 0.0;
		for (int i = 0; i < d; i++)
			sqd += (q.coords[i] - coords[i]) * (q.coords[i] - coords[i]);
		return sqrt(sqd);
	}
};

int point::d;


class cloud
{
private:
	int d;
	int n;
	int k;

	// maximum possible number of points
	int nmax;

	point *points;
	point *centers;

public:
	cloud(int _d, int _nmax, int _k)
	{
		d = _d;
		point::d = _d;
		n = 0;
		k = _k;

		nmax = _nmax;

		points = new point[nmax];
		centers = new point[k];
	}

	~cloud()
	{
		delete[] centers;
		delete[] points;
	}

	void add_point(point &p, int label)
	{
		assert(n < nmax);

		for (int m = 0; m < d; m++)
			points[n].coords[m] = p.coords[m];

		points[n].label = label;

		n++;
	}

	int get_d()
	{
		return d;
	}

	int get_n()
	{
		return n;
	}

	int get_k()
	{
		return k;
	}

	point &get_point(int i)
	{
		return points[i];
	}

	point &get_center(int j)
	{
		return centers[j];
	}

	void set_center(point &p, int j)
	{
		for (int m = 0; m < d; m++)
			centers[j].coords[m] = p.coords[m];
	}

	double intracluster_variance()
	{
		double sum = 0.0;
		for (int i = 0; i < n; i++)
		{
			sum += points[i].dist(centers[points[i].label]) *
				   points[i].dist(centers[points[i].label]);
		}

		return sum / n;
	}

	void set_voronoi_labels()
	{
		for (int i = 0; i < n; i++)
		{
			double min_dist = DBL_MAX;
			int min_ind = -1;

			for (int j = 0; j < k; j++)
			{
				if (points[i].dist(centers[j]) < min_dist)
				{
					min_dist = points[i].dist(centers[j]);
					min_ind = j;
				}
			}
			points[i].label = min_ind;
		}
	}

	void set_centroid_centers()
	{
		int *counts = new int[k];
		for (int j = 0; j < k; j++)
			counts[j] = 0;
		for (int i = 0; i < n; i++)
			counts[points[i].label]++;

		for (int j = 0; j < k; j++)
			if (counts[j] != 0)
				for (int m = 0; m < d; m++)
					centers[j].coords[m] = 0.0;

		for (int i = 0; i < n; i++)
		{
			for (int m = 0; m < d; m++)
				centers[points[i].label].coords[m] += points[i].coords[m];
		}

		for (int j = 0; j < k; j++)
			if (counts[j] != 0)
				for (int m = 0; m < d; m++)
					centers[j].coords[m] /= counts[j];

		delete[] counts;
	}

	void kmeans()
	{

		init_forgy();

		bool stop_changes = false;
		int *old_labels = new int[n];
			

		while (!stop_changes)
		{
			for (int i = 0; i < n; i++)
				old_labels[i] = points[i].label;

			set_voronoi_labels();
			set_centroid_centers();

			bool equal = true;
			for (int i = 0; i < n; i++)
			{
				if (points[i].label != old_labels[i])
				{
					equal = false;
					break;
				}
			}
			stop_changes = equal;
		}
			

		delete[] old_labels;
	}

	void init_forgy()
	{
		int *already_chosen = new int[n];

		for (int j = 0; j < k; j++)
		{

			int i;
			bool new_index = false;
			while (!new_index)
			{
				i = rand() % n;
				new_index = true;
				for (int r = 0; r < j; r++)
					if (already_chosen[r] == i)
					{
						new_index = false;
						break;
					}
			}

			already_chosen[j] = i;

			for (int m = 0; m < d; m++)
				centers[j].coords[m] = points[i].coords[m];
		}

		delete[] already_chosen;
	}
};


/**
 * Counts the number of tab-separated columns in the given line.
 */

int nb_columns(const std::string &line)
{
	return std::count(line.begin(), line.end(), '\t') + 1;
}



int main(int argc, char **argv)
{


	if (argc < 2 || argc > 3)
	{
		std::cerr << "Usage: " << argv[0] << " csv nb_clusters" << std::endl;
		std::exit(1);
	}
	std::string csv_filename = argv[1];
	csv_filename = "test_datasets/"+csv_filename;
	int nb_clusters = std::stoi(argv[2]);


	srand(time(NULL));


	// open data file
	std::ifstream is(csv_filename);
	assert(is.is_open());

	// read header line
	std::string header_line;
	std::getline(is, header_line);
	std::vector<std::string> names;
	std::vector<std::string> list_names;

	const int d = nb_columns(header_line) - 1;
	const int nmax = 150;
	const int k = nb_clusters;
	int n_names = 0;

	// construct point cloud
	cloud c(d, nmax, k);

	// point to read into
	point p;

	// labels to cycle through
	int label = 0;

	// while not at end of file
	while (is.peek() != EOF)
	{
		// read new points
		for (int m = 0; m < d; m++)
		{
			is >> p.coords[m];
		}

		c.add_point(p, label);

		label = (label + 1) % k;

		// read ground-truth labels
		std::string next_name;	
		is >> next_name;

		if (std::find(list_names.begin(), list_names.end(), next_name) == list_names.end())
		{
			list_names.push_back(next_name);
			n_names++;
		}
		names.push_back(next_name);

		// consume \n
		is.get();
	}

	// execute k-means algorithm
	std::cout << "Intracluster variance before k-means: " << c.intracluster_variance() << std::endl;
	c.kmeans();
	std::cout << "Intracluster variance after k-means: " << c.intracluster_variance() << std::endl;


	std::cout << "Saving clustering into \"output.csv\"... " <<std::endl;
	std::ofstream os("output.csv");
	assert(os.is_open());
	os << header_line << '\n';

	//set names of centers - can be optimized
	std::cout << "Names of centers: " << std::endl;
	std::vector<std::string> cluster_names;

	for (int i = 0; i < k; ++i)
	{
		int temp[n_names];
		for(int l = 0; l < n_names; l++) temp [l]=0;

		for (int j = 0; j < c.get_n(); ++j)
		{
			if(c.get_point(j).label == i)
			{
				auto it = std::find(list_names.begin(), list_names.end(), names[j]);
				int index = std::distance(list_names.begin(), it);
				temp[index]++;
			} 
		}
		int m = std::distance(temp, std::max_element(temp, temp + n_names));
		cluster_names.push_back(list_names[m]);
		std::cout<<"label "<< i << " "<< list_names[m] << std::endl;
	}


	double acc = 0.;
	for (int i = 0; i < c.get_n(); ++i)
	{
		for (int j = 0; j < c.get_d(); ++j)
		{
			os << c.get_point(i).coords[j] << '\t';
		}
		os << names[i] << "_Label_" << c.get_point(i).label;
		
		if(names[i] == cluster_names[c.get_point(i).label]) acc++;

		if (i != c.get_n() - 1)
			os << '\n';
	}

	std::cout << "Accuracy: " << acc/(double)c.get_n()*100. <<"%"<< std::endl;
	std::cout << "done" << std::endl;

	return 0;
}

			


