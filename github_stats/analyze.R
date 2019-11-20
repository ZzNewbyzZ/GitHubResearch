popular <- read.csv("Documents/CS599_Research_Methodology/GitHubResearch/data/out_popular.csv")
other <- read.csv("Documents/CS599_Research_Methodology/GitHubResearch/data/out_other.csv")

# Define a function for a binomial proportion test
#  For the binomial proportion test:
#     H0 : There is a difference the proportion of TRUE data in the populations of interest
#     H1 : There is no difference in the proportion of TRUE data in the populations of interest
bpt <- function(a,b){
  p <- as.logical(a)
  o <- as.logical(b)
  sp <- sum(p, na.rm = TRUE)
  so <- sum(o, na.rm = TRUE)
  prop.test(c(sp,so), n=c(length(p),length(o)))
}

bpt(popular$has_pages, other$has_pages)
bpt(popular$has_downloads, other$has_downloads)
bpt(popular$has_issues, other$has_issues)
bpt(popular$has_wiki, other$has_wiki)
bpt(popular$has_projects, other$has_projects)

# Perform Student's t test comparing the means of both groups.
#  H0 : There is a difference in the mean values of the groups' number of open issues
#  H1 : There is no difference in the mean values of the groups' number of open issues
t.test(popular$open_issues_count, other$open_issues_count)

# Perform a chi squared test to compare the frequencies of categorical variables between groups
#  H0 : There is no difference in the frequencies between groups
#  H1 : There is a difference in the frequencies between groups.
chisq.test(popular$language[0:238], other$language[0:238])
