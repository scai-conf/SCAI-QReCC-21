data <- read.csv("scores-test-dataset-2021-07-20.csv")
data.best <- apply(data[,3:11], MARGIN=c(2), max, na.rm=TRUE)
data.rewritten <- read.csv("scores-test-dataset-rewritten-2021-07-20.csv")
data.rewritten.best <- apply(data.rewritten[,3:11], MARGIN=c(2), max, na.rm=TRUE)

mat <- matrix(c(data.best, data.rewritten.best), nrow=2, byrow=TRUE)
colnames(mat) <- gsub("\\.", "-", labels(data.best))

pdf("plot-best.pdf", width=8, height=4)
par(mar=c(5,3,0.1,0))
barplot(mat, beside=T, las=2, legend=c("original", "rewritten"))
lines(c(0,12.5), c(1,1))
lines(c(15.5,28), c(1,1))
dev.off()
