module.exports = {
  title: "Ruby Quest",
  summary: "MSPFA",
  
  edit: true,

  trees: {
    './': 'assets://mspfa/Ruby Quest/',
  },
  async asyncComputed(api) {
    const story = await api.readYamlAsync("./story.yaml")
    return {
      styles: [
        {body: await api.readFileAsync("./adventure.scss")}
      ],
      edit(archive){
        archive.mspfa['Ruby Quest'] = story
      }
    }
  }
}
